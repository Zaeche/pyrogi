if __name__ == "__main__":
    import os
    import tempfile
    file_list = []

    with tempfile.TemporaryDirectory() as temp_path:
        for file in [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]:
            src = os.path.realpath(file)
            if src.endswith((".pdf", ".PDF")):
                dst = f"{temp_path}\\{os.path.basename(src).replace(' ', '_')}"

                import shutil
                shutil.copy(src, dst)
                file_list.append(dst)

        from pikepdf import Pdf, PdfError
        from pikepdf import _cpphelpers
        from glob import glob

        out_file = Pdf.new()
        version = out_file.pdf_version

        for item in sorted(file_list):
            try:
                with Pdf.open(item) as src:
                    version = max(version,src.pdf_version)
                    out_file.pages.extend(src.pages)
            except PdfError:
                import ctypes
                ctypes.windll.user32.MessageBoxW(0, f"Request failed! Could not merge {item}, waaah", "Sad Pyrogie reports...", 0)
                exit()

        from datetime import datetime
        datestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_path = f"_{datestamp}_result.pdf"

        out_file.remove_unreferenced_resources()
        out_file.save(out_path, min_version=version)

        import subprocess
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(out_path,shell=True,creationflags=DETACHED_PROCESS)

"""
References:
    - https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
    - https://stackoverflow.com/questions/3444645/merge-pdf-files
    - https://github.com/pmaupin/pdfrw/blob/master/examples/cat.py
    - http://mstamy2.github.io/PyPDF2/
    - https://pikepdf.readthedocs.io/en/latest/
"""
