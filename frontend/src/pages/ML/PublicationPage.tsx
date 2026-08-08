import { useState } from "react";
import { predictPublication } from "../../api/ml";

export default function PublicationPage() {
    const [title, setTitle] = useState("");
    const [abstract, setAbstract] = useState("");

    // Category state (preset dropdown selection vs custom text)
    const [category, setCategory] = useState("cs");
    const [isCustomCategory, setIsCustomCategory] = useState(false);
    const [customCategory, setCustomCategory] = useState("");

    const [authorCount, setAuthorCount] = useState(1);
    const [commentLength, setCommentLength] = useState(0);
    const [doiExists, setDoiExists] = useState(false);
    const [versionCount, setVersionCount] = useState(1);

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    const handlePredict = async () => {
        try {
            setLoading(true);

            // Determine the final category value based on user's input type
            const finalCategory = isCustomCategory ? customCategory : category;

            const response = await predictPublication({
                title,
                abstract,
                category: finalCategory,
                author_count: authorCount,
                comment_length: commentLength,
                doi_exists: doiExists,
                version_count: versionCount,
            });

            setResult(response.data);
        } catch (err) {
            console.error(err);
            alert("Prediction Failed");
        } finally {
            setLoading(false);
        }
    };

    const handleCategorySelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const val = e.target.value;
        if (val === "custom") {
            setIsCustomCategory(true);
        } else {
            setIsCustomCategory(false);
            setCategory(val);
        }
    };

    return (
        <div className="mx-auto max-w-5xl p-6 text-slate-100">
            <h1 className="mb-8 text-3xl font-bold">Publication Prediction</h1>

            <div className="space-y-6 rounded-xl bg-slate-900 p-6 shadow-xl">
                {/* Paper Title */}
                <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                        Paper Title
                    </label>
                    <input
                        placeholder="Enter research paper title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none focus:border-indigo-500 transition-colors"
                    />
                </div>

                {/* Abstract */}
                <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                        Abstract
                    </label>
                    <textarea
                        rows={6}
                        placeholder="Paste the research paper abstract..."
                        value={abstract}
                        onChange={(e) => setAbstract(e.target.value)}
                        className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none focus:border-indigo-500 transition-colors"
                    />
                </div>

                {/* Primary Category Dropdown + Manual Input Toggle */}
                <div>
                    <div className="mb-2 flex items-center justify-between">
                        <label className="text-sm font-medium text-slate-300">
                            Primary Category
                        </label>
                        <button
                            type="button"
                            onClick={() => {
                                setIsCustomCategory(!isCustomCategory);
                                if (isCustomCategory) setCustomCategory("");
                            }}
                            className="text-xs text-indigo-400 hover:underline"
                        >
                            {isCustomCategory ? "Choose from list" : "+ Enter custom category"}
                        </button>
                    </div>

                    {isCustomCategory ? (
                        <input
                            placeholder="Enter category code (e.g., cs.AI, math.PR)"
                            value={customCategory}
                            onChange={(e) => setCustomCategory(e.target.value)}
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none focus:border-indigo-500 transition-colors"
                        />
                    ) : (
                        <select
                            value={category}
                            onChange={handleCategorySelectChange}
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none focus:border-indigo-500 transition-colors"
                        >
                            <option value="cs">Computer Science (cs)</option>
                            <option value="math">Mathematics (math)</option>
                            <option value="physics">Physics (physics)</option>
                            <option value="stat">Statistics (stat)</option>
                            <option value="econ">Economics (econ)</option>
                            <option value="q-bio">Quantitative Biology (q-bio)</option>
                            <option value="q-fin">Quantitative Finance (q-fin)</option>
                            <option value="eess">Electrical Engineering and Systems Science (eess)</option>
                            <option value="custom">Other / Custom Category...</option>
                        </select>
                    )}
                </div>

                {/* Metadata Inputs */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    {/* Number of Authors */}
                    <div>
                        <label className="mb-2 block text-sm font-medium text-slate-300">
                            Number of Authors
                        </label>
                        <input
                            type="number"
                            min={1}
                            placeholder="e.g. 4"
                            value={authorCount}
                            onChange={(e) => setAuthorCount(Number(e.target.value))}
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none focus:border-indigo-500 transition-colors"
                        />
                    </div>

                    {/* Paper Versions */}
                    <div>
                        <label className="mb-2 block text-sm font-medium text-slate-300">
                            Paper Versions
                        </label>
                        <input
                            type="number"
                            min={1}
                            placeholder="e.g. 1"
                            value={versionCount}
                            onChange={(e) => setVersionCount(Number(e.target.value))}
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none focus:border-indigo-500 transition-colors"
                        />
                    </div>

                    {/* Comment Length */}
                    <div>
                        <label className="mb-2 block text-sm font-medium text-slate-300">
                            Comment Length
                        </label>
                        <input
                            type="number"
                            min={0}
                            placeholder="e.g. 120"
                            value={commentLength}
                            onChange={(e) => setCommentLength(Number(e.target.value))}
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none focus:border-indigo-500 transition-colors"
                        />
                    </div>

                    {/* DOI Available Toggle */}
                    <div>
                        <label className="mb-2 block text-sm font-medium text-slate-300">
                            DOI Available
                        </label>
                        <div className="flex h-[46px] items-center rounded-lg border border-slate-700 bg-slate-800 px-3">
                            <label className="flex cursor-pointer items-center gap-3">
                                <input
                                    type="checkbox"
                                    checked={doiExists}
                                    onChange={(e) => setDoiExists(e.target.checked)}
                                    className="h-4 w-4 rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-indigo-500"
                                />
                                <span className="text-sm text-slate-300">DOI Exists</span>
                            </label>
                        </div>
                    </div>
                </div>

                {/* Submit Button */}
                <button
                    onClick={handlePredict}
                    disabled={loading}
                    className="w-full sm:w-auto rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white transition-colors hover:bg-indigo-500 disabled:opacity-50"
                >
                    {loading ? "Predicting..." : "Predict Publication"}
                </button>
            </div>

            {/* Prediction Output */}
            {result && (
                <div className="mt-8 rounded-xl bg-slate-900 p-6 shadow-xl border border-slate-800">
                    <h2 className="mb-4 text-xl font-bold text-indigo-400">
                        Prediction Result
                    </h2>

                    <div className="space-y-3">
                        <p className="text-slate-200">
                            <strong className="text-slate-400">Status:</strong> {result.status}
                        </p>
                        <p className="text-slate-200">
                            <strong className="text-slate-400">Published:</strong>{" "}
                            <span className={result.published ? "text-emerald-400 font-semibold" : "text-rose-400 font-semibold"}>
                                {result.published ? "Yes" : "No"}
                            </span>
                        </p>
                        <p className="text-slate-200">
                            <strong className="text-slate-400">Probability:</strong>{" "}
                            {result.probability}%
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}