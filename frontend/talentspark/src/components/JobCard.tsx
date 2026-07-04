import type { Job } from "../types/job";

type Props = {
    jobs: Job[];
    onedit: (job: Job) => void;
    ondelete: (id: number) => void;
    onadd: (job: Job) => void;
}

function JobCard({ jobs, onadd, onedit, ondelete }: Props) {
    return (
        <div className="jobs-container">
            <h2>Available Jobs</h2>
            {jobs.length === 0 ? (
                <p>No jobs available</p>
            ) : (
                jobs.map((job) => (
                    <div key={job.id} className="job-card">
                        <h3>{job.title}</h3>
                        <p><strong>Company ID:</strong> {job.company_id}</p>
                        <p><strong>Description:</strong> {job.description}</p>
                        <p><strong>Requirements:</strong> {job.requirements}</p>
                        <p><strong>Salary:</strong> {job.salary}</p>
                        <p><strong>Location:</strong> {job.location}</p>
                        <button onClick={() => onedit(job)}>Edit</button>
                        <button onClick={() => ondelete(job.id)}>Delete</button>
                        <hr />
                    </div>
                ))
            )}
        </div>
    )
}

export default JobCard