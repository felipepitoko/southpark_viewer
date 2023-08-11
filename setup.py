from cx_Freeze import setup, Executable
import os,shutil

builds = os.listdir('build')
for vers in builds:
    shutil.rmtree('build/'+vers)

build_exe_options = {
    "includes": [],
    "include_files": ['database.db'],
    # Other build options can be added here if needed
}

setup(
    name="SouthparkViewer",
    version="0.1",
    options={"build_exe": build_exe_options},
    description="Pequeno app para maratonar southpark",
    executables=[Executable("tela.py")]
)