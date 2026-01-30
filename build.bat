@echo off
echo ======================================================
echo   DICH THUAT PRO - DONG GOI UNG DUNG
echo ======================================================

echo [1/3] Dang kiem tra va cai dat thu vien...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/3] Dang bat dau dong goi (Vui long doi trong giay lat)...
echo Chế độ: OneFile, NoConsole
pyinstaller --noconsole --onefile --name "DichThuat_Pro" translate.py

echo.
echo [3/3] Hoan thanh!
echo ------------------------------------------------------
echo File .exe cua ban nam trong thu muc: [dist]
echo Ban co the copy file DichThuat_Pro.exe ra ngoai de su dung.
echo ------------------------------------------------------
pause
