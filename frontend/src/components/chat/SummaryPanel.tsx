type Props = {
    summary: string;
};

export default function SummaryPanel({
    summary,
}: Props) {

    if (!summary) return null;

    return (

        <div className="border-b border-slate-800 bg-slate-900 p-4">

            <h3 className="mb-2 text-lg font-semibold">

                Chat Summary

            </h3>

            <p className="text-slate-300">

                {summary}

            </p>

        </div>

    );

}