import { Upload } from "lucide-react";

type Props = {
    onUpload: (file: File) => void;
};

export default function UploadButton({
    onUpload,
}: Props) {
    return (
        <label className="cursor-pointer rounded-lg border border-slate-700 px-4 py-2 hover:bg-slate-800">

            <input
                hidden
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(e) => {
                    if (e.target.files?.length) {
                        onUpload(e.target.files[0]);
                    }
                }}
            />

            <div className="flex items-center gap-2">

                <Upload size={18} />

                Upload

            </div>

        </label>
    );
}