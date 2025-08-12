
# setup
```bash
init --python=3.11
uv sync
# uv add ipykernel
uv pip install ipykernel
uv pip install pyinstaller
```


# export(pyinstaller)
```bash
--add-data other static file.

uv run pyinstaller --onefile \
    --name template_paste \
    --distpath  ~/.local/bin/ \
    --specpath /tmp/ \
    main.py
```