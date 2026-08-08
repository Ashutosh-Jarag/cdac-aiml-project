import { useState } from "react";
import { classifyPaper } from "../../api/ml";

export default function ClassificationPage() {

    const [title, setTitle] = useState("");

    const [abstract, setAbstract] = useState("");

    const [loading, setLoading] = useState(false);

    const [categories, setCategories] = useState<
        { code: string; name: string }[]
    >([]);

    const handlePredict = async () => {

        try {

            setLoading(true);

            const response = await classifyPaper(
                title,
                abstract
            );

            setCategories(
                response.data.categories
            );

        } catch (error) {

            console.error(error);

            alert("Prediction failed");

        } finally {

            setLoading(false);

        }
    };

    return (

        <div className="mx-auto max-w-5xl">

            <h1 className="mb-8 text-3xl font-bold">
                Research Paper Classification
            </h1>

            <div className="space-y-6 rounded-xl bg-slate-900 p-6">

                <div>

                    <label className="mb-2 block">
                        Title
                    </label>

                    <input
                        value={title}
                        onChange={(e) =>
                            setTitle(e.target.value)
                        }
                        className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none"
                    />

                </div>

                <div>

                    <label className="mb-2 block">
                        Abstract
                    </label>

                    <textarea
                        rows={8}
                        value={abstract}
                        onChange={(e) =>
                            setAbstract(e.target.value)
                        }
                        className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 outline-none"
                    />

                </div>

                <button
                    onClick={handlePredict}
                    disabled={loading}
                    className="rounded-lg bg-indigo-600 px-6 py-3 hover:bg-indigo-700 disabled:opacity-50"
                >

                    {loading
                        ? "Predicting..."
                        : "Predict Category"}

                </button>

            </div>

            {categories.length > 0 && (

                <div className="mt-8 rounded-xl bg-slate-900 p-6">

                    <h2 className="mb-4 text-xl font-semibold">
                        Prediction
                    </h2>

                    <div className="flex flex-wrap gap-4">

                        {categories.map((category) => (

                            <div
                                key={category.code}
                                className="rounded-lg bg-indigo-500/20 px-5 py-4"
                            >

                                <div className="text-lg font-semibold">

                                    {category.name}

                                </div>

                                <div className="text-sm text-slate-400">

                                    {category.code}

                                </div>

                            </div>

                        ))}

                    </div>

                </div>

            )}

        </div>

    );
}