$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Open("C:\Users\zhangfan\Desktop\武将品质划分_v21.xlsx")
$ws = $wb.Sheets.Item("武将名单")

# 获取数据范围
$maxRow = $ws.UsedRange.Rows.Count
$maxCol = $ws.UsedRange.Columns.Count

Write-Host "总行数: $maxRow, 总列数: $maxCol"
Write-Host "---"

# 获取列标题
$headers = @()
for ($col = 1; $col -le $maxCol; $col++) {
    $headers += $ws.Cells.Item(1, $col).Text
}
Write-Host "列名: $($headers -join ', ')"

# 输出所有数据
for ($row = 1; $row -le $maxRow; $row++) {
    $rowData = @()
    for ($col = 1; $col -le $maxCol; $col++) {
        $rowData += $ws.Cells.Item($row, $col).Text
    }
    Write-Host ($rowData -join "`t")
}

$wb.Close($false)
$excel.Quit()
