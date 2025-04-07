
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Button, Container } from '@mui/material';
import BookingPage from './pages/BookingPage';
import InventoryPage from './pages/InventoryPage';
import StaffPage from './pages/StaffPage';
import ReportsPage from './pages/ReportsPage';
import CustomerChatPage from './pages/CustomerChatPage';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">Booking</Button>
          <Button color="inherit" component={Link} to="/inventory">Inventory</Button>
          <Button color="inherit" component={Link} to="/staff">Staff</Button>
          <Button color="inherit" component={Link} to="/reports">Reports</Button>
          <Button color="inherit" component={Link} to="/chat">Customer Chat</Button>
        </Toolbar>
      </AppBar>
      <Container style={{ marginTop: '2em' }}>
        <Routes>
          <Route path="/" element={<BookingPage />} />
          <Route path="/inventory" element={<InventoryPage />} />
          <Route path="/staff" element={<StaffPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/chat" element={<CustomerChatPage />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
