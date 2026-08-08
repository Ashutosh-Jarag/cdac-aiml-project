import { useState } from "react";
import { recommendPapers } from "../../api/ml";

export default function RecommendationPage() {

  const [title, setTitle] = useState("");

  const [abstract, setAbstract] = useState("");

  const [topK, setTopK] = useState(5);

  const [papers, setPapers] = useState<any[]>([]);

  const [loading, setLoading] = useState(false);

  async function handleRecommend() {

    try {

      setLoading(true);

      const response = await recommendPapers(
        title,
        abstract,
        topK
      );

      setPapers(response.data.papers);

    } finally {

      setLoading(false);

    }

  }

  return (

    <div className="mx-auto max-w-6xl">

      <h1 className="mb-8 text-3xl font-bold">
        Paper Recommendation
      </h1>

      <div className="space-y-5 rounded-xl bg-slate-900 p-6">

        <div>

          <label className="mb-2 block">
            Paper Title
          </label>

          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter paper title"
            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3"
          />

        </div>

        <div>

          <label className="mb-2 block">
            Abstract
          </label>

          <textarea
            rows={6}
            value={abstract}
            onChange={(e) => setAbstract(e.target.value)}
            placeholder="Paste abstract..."
            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3"
          />

        </div>

        <div>

          <label className="mb-2 block">
            Number of Recommendations
          </label>

          <select
            value={topK}
            onChange={(e) => setTopK(Number(e.target.value))}
            className="rounded-lg border border-slate-700 bg-slate-800 p-3"
          >

            <option value={3}>3</option>
            <option value={5}>5</option>
            <option value={10}>10</option>

          </select>

        </div>

        <button
          onClick={handleRecommend}
          className="rounded-lg bg-indigo-600 px-6 py-3"
        >

          {loading
            ? "Searching..."
            : "Recommend Papers"}

        </button>

      </div>

      {papers.length > 0 && (

        <div className="mt-8 space-y-5">

          {papers.map((paper, index) => (

            <div
              key={index}
              className="rounded-xl bg-slate-900 p-6"
            >

              <h2 className="text-xl font-semibold">

                {paper.title}

              </h2>

              <p className="mt-2 text-slate-400">

                {paper.authors}

              </p>

              <p>

                Category :
                {" "}
                {paper.category}

              </p>

              <p>

                Similarity :
                {" "}
                {paper.similarity}%

              </p>

              <a
                href={paper.paper_url}
                target="_blank"
                className="mt-3 inline-block text-indigo-400"
              >

                View Paper →

              </a>

            </div>

          ))}

        </div>

      )}

    </div>

  );

}