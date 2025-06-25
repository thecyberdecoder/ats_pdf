import React from 'react';
import PDFMerge from './components/PDFMerge';
import PDFSplit from './components/PDFSplit';
import PDFCompress from './components/PDFCompress';
import PDFRotate from './components/PDFRotate';
import PDFConvert from './components/PDFConvert';
import { Container, Tabs, Tab } from '@mui/material';

function App() {
  const [tab, setTab] = React.useState(0);
  const features = [
    { label: "Merge PDF", component: <PDFMerge /> },
    { label: "Split PDF", component: <PDFSplit /> },
    { label: "Compress PDF", component: <PDFCompress /> },
    { label: "Rotate PDF", component: <PDFRotate /> },
    { label: "Convert", component: <PDFConvert /> },
  ];
  return (
    <Container>
      <h1>ATS PDF Web Toolkit</h1>
      <Tabs value={tab} onChange={(_, v) => setTab(v)}>
        {features.map((f, i) => <Tab key={i} label={f.label} />)}
      </Tabs>
      <div style={{ marginTop: 32 }}>{features[tab].component}</div>
    </Container>
  );
}
export default App;