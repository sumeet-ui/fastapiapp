import axios from "axios";
import type { Job } from "../types/job";

const API_BASE_URL ="http://localhost:8000";

export async function getCompanies(): Promise<Job[]> { 
    const response = await axios.get(`${API_BASE_URL}/company`);
    return response.data;
}

export async function getjob(id: number): Promise<Job> {
  const response = await axios.get(`${API_BASE_URL}/company/${id}`);
  return response.data;
}


export async function createJob(job : Job): Promise<Job> {
    const response = await axios.post(`${API_BASE_URL}/company`,job);
    return response.data;
}

export async function updateJob(id: number,company:Job): Promise<Job> {
    const response = await axios.put(`${API_BASE_URL}/company/${id}`,company);
    return response.data;
}

export async function deleteJob(id: number): Promise<Job> {
    const response = await axios.delete(`${API_BASE_URL}/company/${id}`);
    return response.data;
}