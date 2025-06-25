import React, { useState } from 'react';
import { Button, Typography, Box, CircularProgress } from '@mui/material';

function PDFMerge() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFiles = e => setFiles([...e.target.files]);
  const handleMerge = async () => {
    setLoading(true);
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    const res = await fetch('/api/pdf/merge', { method: 'POST', body: formData });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'merged.pdf'; a.click();
    setLoading(false);
  };
  return (
    <Box>
      <Typography variant="h5">Merge PDF</Typography>
      <input type="file" accept="application/pdf" multiple onChange={handleFiles} />
      <Button disabled={!files.length || loading} onClick={handleMerge}>
        Merge
      </Button>
      {loading && <CircularProgress />}
    </Box>
  );
}

export default PDFMerge;