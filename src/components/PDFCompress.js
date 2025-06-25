import React, { useState } from 'react';
import { Button, Typography, Box, Slider, CircularProgress } from '@mui/material';

function PDFCompress() {
  const [file, setFile] = useState(null);
  const [quality, setQuality] = useState(60);
  const [loading, setLoading] = useState(false);

  const handleFile = e => setFile(e.target.files[0]);
  const handleCompress = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('quality', quality);
    const res = await fetch('/api/pdf/compress', { method: 'POST', body: formData });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'compressed.pdf'; a.click();
    setLoading(false);
  };
  return (
    <Box>
      <Typography variant="h5">Compress PDF</Typography>
      <input type="file" accept="application/pdf" onChange={handleFile} />
      <Slider
        value={quality}
        onChange={(_, val) => setQuality(val)}
        min={10}
        max={100}
        step={1}
        sx={{ width: 300 }}
        valueLabelDisplay="auto"
      />
      <Button disabled={!file || loading} onClick={handleCompress}>
        Compress
      </Button>
      {loading && <CircularProgress />}
    </Box>
  );
}

export default PDFCompress;