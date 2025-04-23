
# Hi-Line PDF Generator API

This Flask API generates customer statement PDFs from an uploaded Excel file and logo, returning a ZIP file. Matches the Hi-Line locked-in format.

## Usage

**POST** to `/generate` with:
- `excel`: Excel file (.xlsx) with a sheet named `5 Data Only`
- `logo`: Company logo (JPG)

Returns:
- A ZIP file with one PDF per customer

## Example (cURL)

```
curl -X POST http://localhost:5000/generate \
  -F "excel=@Statement.xlsx" \
  -F "logo=@logo.jpg" \
  -o statements.zip
```

## Deployment (Render)

1. Create a new GitHub repo and upload:
   - `hi_line_pdf_api.py`
   - `requirements.txt`
   - `README.md`
2. Go to [https://render.com](https://render.com)
3. Click "New Web Service" → Connect your GitHub
4. Set:
   - Runtime: Python 3.10+
   - Start command: `python hi_line_pdf_api.py`
   - Free instance type
