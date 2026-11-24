"""
PodX Desktop Shortcut & Icon Generator
Creates high-resolution .ico logo and generates a Windows Desktop shortcut.
"""
import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

def create_logo_ico(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    ico_path = output_dir / "podx.ico"
    png_path = output_dir / "podx_logo.png"

    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Background Rounded Rect with gradient-like solid glow
    # Outer glow
    for r in range(240, 210, -5):
        alpha = int((r - 210) * 1.5)
        draw.rounded_rectangle([256 - r, 256 - r, 256 + r, 256 + r], radius=85, outline=(139, 92, 246, alpha), width=3)

    # Main dark rounded square
    draw.rounded_rectangle([50, 50, 462, 462], radius=85, fill=(17, 20, 24, 255), outline=(139, 92, 246, 255), width=8)

    # Inner subtle background fill
    draw.rounded_rectangle([58, 58, 454, 454], radius=80, fill=(26, 19, 48, 255))

    # 2. Sound Wave Arcs (Left & Right)
    # Left arcs
    draw.arc([110, 160, 230, 320], start=110, end=250, fill=(6, 182, 212, 255), width=8)
    draw.arc([75, 130, 230, 350], start=110, end=250, fill=(139, 92, 246, 255), width=8)

    # Right arcs
    draw.arc([282, 160, 402, 320], start=290, end=70, fill=(6, 182, 212, 255), width=8)
    draw.arc([282, 130, 437, 350], start=290, end=70, fill=(139, 92, 246, 255), width=8)

    # 3. Studio Microphone Capsule
    # Mic body
    draw.rounded_rectangle([216, 140, 296, 275], radius=40, fill=(139, 92, 246, 255), outline=(192, 132, 252, 255), width=6)
    
    # Mic grille lines
    for y in [175, 200, 225]:
        draw.line([226, y, 286, y], fill=(230, 210, 255, 255), width=4)

    # Mic U-mount / cradle
    draw.arc([188, 190, 324, 310], start=0, end=180, fill=(245, 243, 255, 255), width=8)

    # Vertical stem
    draw.line([256, 310, 256, 360], fill=(245, 243, 255, 255), width=8)

    # Stand base
    draw.rounded_rectangle([195, 360, 317, 376], radius=8, fill=(245, 243, 255, 255))

    # Small neon studio dot
    draw.ellipse([248, 105, 264, 121], fill=(6, 182, 212, 255))

    # Save high-res PNG
    img.save(png_path, format="PNG")

    # Save multi-size ICO
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(ico_path, format="ICO", sizes=icon_sizes)

    print(f"Created icon assets:\n  PNG: {png_path}\n  ICO: {ico_path}")
    return ico_path, png_path

def create_windows_shortcut(ico_path: Path):
    base_dir = Path(__file__).resolve().parent.parent
    launcher_bat = base_dir / "PodX_Studio.bat"
    
    # Create the one-click launcher batch file
    bat_content = f"""@echo off
title PodX - Elite Knowledge AI Podcast Studio
cd /d "{base_dir}"

echo =================================================================
echo          PodX -- Elite Knowledge AI Podcast Studio
echo =================================================================
echo.
echo Starting PodX Studio Server on http://127.0.0.1:8001 ...
echo Opening your default browser...

start "" "http://127.0.0.1:8001"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001

pause
"""
    with open(launcher_bat, "w", encoding="utf-8") as f:
        f.write(bat_content)

    # Create shortcut on User Desktop via PowerShell
    ps_cmd = f"""
$desktop = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
if (-not (Test-Path $desktop)) {{
    $desktop = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
}}
$shortcutPath = [System.IO.Path]::Combine($desktop, "PodX — AI Podcast Studio.lnk")
$wscript = New-Object -ComObject WScript.Shell
$shortcut = $wscript.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "{launcher_bat.as_posix()}"
$shortcut.WorkingDirectory = "{base_dir.as_posix()}"
$shortcut.IconLocation = "{ico_path.as_posix()}, 0"
$shortcut.Description = "Launch PodX - Elite Knowledge AI Podcast Studio"
$shortcut.Save()

Write-Output "SHORTCUT_CREATED: $shortcutPath"
"""
    result = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_cmd], encoding="utf-8").strip()
    print(result)

if __name__ == "__main__":
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    ico, png = create_logo_ico(assets_dir)
    create_windows_shortcut(ico)
