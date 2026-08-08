import {
    MessageSquare,
    Brain,
    FileSearch,
    BookOpen,
    Database,
    Cpu,
} from "lucide-react";

const features = [
    {
        title: "AI Research Chat",
        description:
            "Chat with uploaded research documents using document-based retrieval and AI-generated answers.",
        icon: MessageSquare,
    },
    {
        title: "Research Classification",
        description:
            "Classifies research documents into their relevant academic category using a trained SVM model.",
        icon: Brain,
    },
    {
        title: "Publication Prediction",
        description:
            "Predicts the probability of a research paper being published using machine learning features.",
        icon: FileSearch,
    },
    {
        title: "Research Recommendation",
        description:
            "Finds similar research papers from the arXiv dataset using Sentence-BERT and Pinecone.",
        icon: BookOpen,
    },
    {
        title: "ML Research Chat",
        description:
            "Provides research-oriented answers using semantic retrieval from the research paper knowledge base.",
        icon: Database,
    },
];

const technologies = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "SVM",
    "XGBoost",
    "Sentence-BERT",
    "Pinecone",
    "ChromaDB",
    "Gemini",
    "NLTK",
    "React",
];

export default function DashboardPage() {
    return (
        <div className="h-full overflow-y-auto bg-slate-950 p-6">

            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white">
                    ResearchAI
                </h1>

                <p className="mt-2 max-w-3xl text-slate-400">
                    An AI and machine learning platform for
                    research document analysis, classification,
                    publication prediction, recommendation,
                    and research-oriented question answering.
                </p>
            </div>

            {/* Project Overview */}
            <div className="mb-8 rounded-xl border border-slate-800 bg-slate-900 p-6">

                <div className="flex items-center gap-3 mb-4">
                    <Cpu
                        size={22}
                        className="text-indigo-400"
                    />

                    <h2 className="text-xl font-semibold text-white">
                        Project Overview
                    </h2>
                </div>

                <p className="leading-7 text-slate-400">
                    ResearchAI combines document processing,
                    machine learning, semantic search, vector
                    databases, and generative AI to assist users
                    in exploring and understanding research
                    documents and papers.
                </p>

            </div>

            {/* Features */}
            <div className="mb-8">

                <h2 className="mb-4 text-xl font-semibold text-white">
                    Available Features
                </h2>

                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

                    {features.map((feature) => {

                        const Icon = feature.icon;

                        return (
                            <div
                                key={feature.title}
                                className="rounded-xl border border-slate-800 bg-slate-900 p-5 hover:border-slate-700"
                            >

                                <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-500/10">
                                    <Icon
                                        size={20}
                                        className="text-indigo-400"
                                    />
                                </div>

                                <h3 className="mb-2 font-semibold text-white">
                                    {feature.title}
                                </h3>

                                <p className="text-sm leading-6 text-slate-400">
                                    {feature.description}
                                </p>

                            </div>
                        );
                    })}

                </div>

            </div>

            {/* Technology Stack */}
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

                <h2 className="mb-4 text-xl font-semibold text-white">
                    Technology Stack
                </h2>

                <div className="flex flex-wrap gap-2">

                    {technologies.map((technology) => (
                        <span
                            key={technology}
                            className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-300"
                        >
                            {technology}
                        </span>
                    ))}

                </div>

            </div>

        </div>
    );
}