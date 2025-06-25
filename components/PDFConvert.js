import React, { useState } from 'react';
import { Button, Typography, Box, Select, MenuItem, CircularProgress, InputLabel, FormControl } from '@mui/material';

const formats = [
  { label: "PDF", value: "pdf" },
  { label: "Word (DOCX)", value: "docx" },
  { label: "Excel (XLSX)", value: "xlsx" },
  { label: "PowerPoint (PPTX)", value: "pptx" },
  { label: "JPG Image", value: "jpg" },
  { label: "PDF/A", value: "pdfa" },
  { label: "HTML", value: "html" }
];

function PDFConvert() {
  const [file, setFile] = useState(null);
  const [fromType, setFromType] = useState("pdf");
  const [toType, setToType] = useState("docx");
  const [loading, setLoading] = useState(false);

  const handleFile = e => setFile(e.target.files[0]);
  const handleConvert = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('from_type', fromType);
    formData.append('to_type', toType);
    const res = await fetch('/api/pdf/convert', { method: 'POST', body: formData });
    if (res.headers.get("content-type")?.includes("application/json")) {
      alert("Conversion not supported or failed.");
      setLoading(false);
      return;
    }
    const blob = await res.blob();
    const ext = toType === "jpg" ? "zip" : toType;
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `converted.${ext}`; a.click();
    setLoading(false);
  };
  return (
    <Box>
      <Typography variant="h5">Convert Document</Typography>
      <input type="file" onChange={handleFile} />
      <FormControl margin="normal" sx={{ minWidth: 120 }}>
        <InputLabel>From</InputLabel>
        <Select value={fromType} label="From" onChange={e => setFromType(e.target.value)}>
          {formats.map(f => <MenuItem key={f.value} value={f.value}>{f.label}</MenuItem>)}
        </Select>
      </FormControl>
      <FormControl margin="normal" sx={{ minWidth: 120 }}>
        <InputLabel>To</InputLabel>
        <Select value={toType} label="To" onChange={e => setToType(e.target.value)}>
          {formats.map(f => <MenuItem key={f.value} value={f.value}>{f.label}</MenuItem>)}
        </Select>
      </FormControl>
      <Button disabled={!file || !fromType || !toType || loading} onClick={handleConvert}>
        Convert
      </Button>
      {loading && <CircularProgress />}
    </Box>
  );
}

export default PDFConvert;