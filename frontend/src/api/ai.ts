import client from "./client";

/* ---------- Upload ---------- */

export const uploadDocument = async (file: File) => {
    const formData = new FormData();

    formData.append("file", file);

    const { data } = await client.post(
        "/ai/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return data;
};

/* ---------- Chat ---------- */

export const sendMessage = async (
    sessionId: string,
    message: string,
    provider = "gemini",
    apiKey?: string
) => {
    const { data } = await client.post("/ai/chat", {
        session_id: sessionId,
        message,
        provider,
        api_key: apiKey,
    });

    return data;
};

/* ---------- Sessions ---------- */

export const getSessions = async () => {
    const { data } = await client.get("/ai/sessions");

    return data;
};

export const getHistory = async (
    sessionId: string
) => {
    const { data } = await client.get(
        `/ai/history/${sessionId}`
    );

    return data;
};

export const renameSession = async (
    sessionId: string,
    title: string
) => {
    const { data } = await client.put(
        `/ai/sessions/${sessionId}`,
        {
            title,
        }
    );

    return data;
};

export const deleteSession = async (
    sessionId: string
) => {
    const { data } = await client.delete(
        `/ai/sessions/${sessionId}`
    );

    return data;
};

/* ---------- Summary ---------- */

export const summarizeChat = async (
    sessionId: string,
    mode: "short" | "long" = "short"
) => {
    const { data } = await client.post(
        "/ai/summary",
        {
            session_id: sessionId,
            mode,
        }
    );

    return data;
};