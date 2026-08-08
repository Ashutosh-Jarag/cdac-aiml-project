import { User } from "lucide-react";

export default function ProfilePage() {
    return (
        <div className="h-full overflow-y-auto bg-slate-950 p-6">

            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white">
                    Profile
                </h1>

                <p className="mt-2 text-slate-400">
                    Manage your profile information.
                </p>
            </div>

            <div className="max-w-2xl rounded-xl border border-slate-800 bg-slate-900 p-6">

                <div className="mb-6 flex items-center gap-3">
                    <User
                        size={20}
                        className="text-indigo-400"
                    />

                    <h2 className="font-semibold text-white">
                        Profile Information
                    </h2>
                </div>

                <div className="space-y-5">

                    <div>
                        <label className="mb-2 block text-sm text-slate-400">
                            Name
                        </label>

                        <input
                            type="text"
                            placeholder="Your name"
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
                        />
                    </div>

                    <div>
                        <label className="mb-2 block text-sm text-slate-400">
                            Email
                        </label>

                        <input
                            type="email"
                            placeholder="Your email"
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
                        />
                    </div>

                    <button
                        className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-indigo-500"
                    >
                        Save Changes
                    </button>

                </div>

            </div>

        </div>
    );
}