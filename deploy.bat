pyinstaller --onefile --windowed --icon=icon.ico main.py
for %%f in (*.png) do (
    copy /Y "%%f" "dist\"
)
for %%f in (*.json) do (
    copy /Y "%%f" "dist\"
)
for %%f in (*.ico) do (
    copy /Y "%%f" "dist\"
)
echo Deployment complete!