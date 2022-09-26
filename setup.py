import cx_Freeze

executables = [cx_Freeze.Executable("Teste01.py")]

cx_Freeze.setup(name="DinoGame", options={"build_exe":{"packages":["pygame"], "include_files":["imagens", "sons"]}}, executables = executables
)
