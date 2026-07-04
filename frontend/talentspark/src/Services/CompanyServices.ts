import axios from "axios";
import type {Company} from "../types/company";

const API_BASE_URL ="http://localhost:8000";

// Helper to get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem("access_token");
    return {
        Authorization: `Bearer ${token}`
    };
}

export async function getCompanies(): Promise<Company[]> { 
    const response = await axios.get(`${API_BASE_URL}/company`, {
        headers: getAuthHeaders()
    });
    return response.data;
}

export async function getCompany(id: number): Promise<Company> {
  const response = await axios.get(`${API_BASE_URL}/company/${id}`, {
    headers: getAuthHeaders()
  });
  return response.data;
}


export async function createCompany(company : Company): Promise<Company> {
    const response = await axios.post(`${API_BASE_URL}/company`, company, {
        headers: getAuthHeaders()
    });
    return response.data;
}

export async function updateCompany(id: number,company:Company): Promise<Company> {
    const response = await axios.put(`${API_BASE_URL}/company/${id}`, company, {
        headers: getAuthHeaders()
    });
    return response.data;
}

export async function deleteCompany(id: number): Promise<void> {
    const response = await axios.delete(`${API_BASE_URL}/company/${id}`, {
        headers: getAuthHeaders()
    });
    return response.data;
}