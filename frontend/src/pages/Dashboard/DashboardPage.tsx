import PageHeader from "../../components/layout/PageHeader";

export default function DashboardPage() {
    return (
        <div>

            <PageHeader
                title="Dashboard"
                description="Overview of your ResearchAI platform."
            />

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-8">

                <h2 className="mb-4 text-2xl font-semibold">

                    🚧 Coming Soon

                </h2>

                <ul className="space-y-2 text-slate-400">

                    <li>• Chat Analytics</li>

                    <li>• Uploaded Documents</li>

                    <li>• Machine Learning Statistics</li>

                    <li>• AI Usage</li>

                    <li>• Recent Activity</li>

                    <li>• Search Analytics</li>

                </ul>

            </div>

        </div>
    );
}