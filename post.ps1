$Url = "http://localhost:5000/api/test.txt"
$Body = @{
    owner = 0
    permissions = "-rwxr-xr-x"
    content = "testing 123"
    type = "file"
}
Invoke-RestMethod -Method 'POST' -Uri $url -Body $body
