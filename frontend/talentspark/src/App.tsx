import NavBar from "./components/NavBar";
import Welcome from "./components/Welcome";
import Footer from "./components/Footer";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import {useState,useEffect} from "react";
import { getCompanies } from "./Services/CompanyServices";
import { getJobs } from "./Services/JobServices";
import type { Company } from "./types/company";
import type { Job } from "./types/job";

function App() {
  const[loading,setLoading]=useState(true);
  const[error,setError]=useState<Error|null>(null);
  const[companies,setCompanies]=useState<Company[]>([]);
  const[jobs,setJobs]=useState<Job[]>([]);
  const[isLoggedIn,setIsLoggedIn]=useState(false);

  async function fetchCompanies(){
    try{
      const companies=await getCompanies();
      setCompanies(companies);
    } catch (err) {
      setError(err as Error);
    }
  }

  async function fetchJobs(){
    try{
      const jobs=await getJobs();
      setJobs(jobs);
    } catch (err) {
      setError(err as Error);
    }
  }

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("access_token");
    if(token){
      setIsLoggedIn(true);
      setLoading(true);
      Promise.all([fetchCompanies(), fetchJobs()]).finally(() => {
        setLoading(false);
      });
    } else {
      setIsLoggedIn(false);
      setLoading(false);
    }
  }, []);

  const handleAddCompany = (company: Company) => {
    setCompanies([...companies, company]);
  };

  const handleEditCompany = (company: Company) => {
    setCompanies(companies.map(c => c.id === company.id ? company : c));
  };

  const handleDeleteCompany = (id: number) => {
    setCompanies(companies.filter(c => c.id !== id));
  };

  const handleAddJob = (job: Job) => {
    setJobs([...jobs, job]);
  };

  const handleEditJob = (job: Job) => {
    setJobs(jobs.map(j => j.id === job.id ? job : j));
  };

  const handleDeleteJob = (id: number) => {
    setJobs(jobs.filter(j => j.id !== id));
  };

  if(loading){
    return <div>Loading...</div>;
  }

  if(!isLoggedIn){
    return (
      <>
        <NavBar />
        <Welcome />
        <div style={{textAlign: 'center', padding: '50px'}}>
          <h2>Please login to view companies and jobs</h2>
        </div>
        <Footer />
      </>
    );
  }

  if(error){
    return <div>Error: {error.message}</div>;
  }

  return (
    <>
      <NavBar />
      <Welcome />
      <CompanyCard 
        companies={companies} 
        onadd={handleAddCompany}
        onedit={handleEditCompany}
        ondelete={handleDeleteCompany}
      />
      <JobCard 
        jobs={jobs}
        onadd={handleAddJob}
        onedit={handleEditJob}
        ondelete={handleDeleteJob}
      />
      <Footer />
    </>
  );
}
  
export default App;