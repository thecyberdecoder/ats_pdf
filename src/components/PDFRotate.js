import React, { useState } from 'react';
import { Button, Typography, Box, Slider, CircularProgress } from '@mui/material';

function PDFRotate() {
  const [file, setFile] = useState(null);
  const [angle, setAngle] = useState(90);
  const [loading, setLoading] = useState(false);

  const handleFile = e => setFile(e.target.files[0]);
  const handleRotate = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('angle', angle);
    const res = await fetch('/api/pdf/rotate', { method: 'POST', body: formData });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'rotated.pdf'; a.click();
    setLoading(false);
  };
  return (
    <Box>
      <Typography variant="h5">Rotate PDF</Typography>
      <input type="file" accept="application/pdf" onChange={handleFile} />
      <Slider
        value={angle}
        onChange={(_, val) => setAngle(val)}
        min={-180}
        max={180}
        step={90}
        marks
        sx={{ width: 300 }}
        valueLabelDisplay="auto"
      />
      <Button disabled={!file || loading} onClick={handleRotate}>
        Rotate
      </Button>
      {loading && <CircularProgress />}
    </Box>
  );
}

export default PDFRotate;