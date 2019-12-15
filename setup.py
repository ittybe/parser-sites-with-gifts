from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'include_msvcr': True,
    }
}
zip_include_packages = ['collections', 'encodings', 'importlib', 'requests', 'bs4', 'PyQt5']
setup(
    name="parser",
    version="0.1",
    description="main",
    executables=[Executable("main.py")]
)