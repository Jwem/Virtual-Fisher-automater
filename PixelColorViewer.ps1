Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Write-Host "Real-time pixel color viewer: Press CTRL+C to exit."
while ($true) {
    $pos = [System.Windows.Forms.Cursor]::Position
    $bitmap = New-Object System.Drawing.Bitmap(1,1)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($pos, [System.Drawing.Point]::Empty, $bitmap.Size)
    $color = $bitmap.GetPixel(0,0)
    Clear-Host
    Write-Host "Position: ($($pos.X), $($pos.Y))"
    Write-Host "Color (RGB): ($($color.R), $($color.G), $($color.B))"
    Start-Sleep -Milliseconds 100
}
