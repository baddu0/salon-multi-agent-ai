
import axios from 'axios';

const API_BASE = 'http://localhost:5000';

export const getBookings = () => axios.get(`${API_BASE}/scheduler`);
export const getInventory = () => axios.get(`${API_BASE}/inventory`);
export const getStaff = () => axios.get(`${API_BASE}/staff`);
export const getReports = () => axios.get(`${API_BASE}/reporting`);
export const getCustomerMessages = () => axios.get(`${API_BASE}/customer_service`);

export const createBooking = (data) => axios.post(`${API_BASE}/scheduler`, data);
export const updateInventory = (data) => axios.post(`${API_BASE}/inventory`, data);
export const updateStaff = (data) => axios.post(`${API_BASE}/staff`, data);
export const sendCustomerMessage = (data) => axios.post(`${API_BASE}/customer_service`, data);
