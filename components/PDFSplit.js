import React, { useState } from 'react';
import { Button, Typography, Box, TextField, CircularProgress } from '@mui/material';

function PDFSplit() {
  const [file, setFile] = useState(null);
  const [ranges, setRanges] = useState('1-1');
  const [loading, setLoading] = useState(false);

  const handleFile = e => setFile(e.target.files[0]);
  const handleSplit = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('ranges', ranges);
    const res = await fetch('/api/pdf/split', { method: 'POST', body: formData });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'splits.zip'; a.click();
    setLoading(false);
  };
  return (
    <Box>
      <Typography variant="h5">Split PDF</Typography>
      <input type="file" accept="application/pdf" onChange={handleFile} />
      <TextField
        label="Ranges (e.g. 1-2,3-3,4-6)"
        value={ranges}
        onChange={e => setRanges(e.target.value)}
        helperText="Enter page ranges for each split, comma separated."
        margin="normal"
        fullWidth
      />
      <Button disabled={!file || loading} onClick={handleSplit}>
        Split
      </Button>
      {loading && <CircularProgress />}
    </Box>
  );
}

export default PDFSplit;