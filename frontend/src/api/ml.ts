import client from "./client";

export const classifyPaper = async (
    title: string,
    abstract: string
) => {

    const { data } = await client.post(
        "/ml/classification",
        {
            title,
            abstract,
        }
    );

    return data;
};


export const predictPublication = async (payload: {
    title: string;
    abstract: string;
    category: string;
    author_count: number;
    comment_length: number;
    doi_exists: boolean;
    version_count: number;
}) => {

    const { data } = await client.post(
        "/ml/publication",
        payload
    );

    return data;
};

export const recommendPapers = async (
    title: string,
    abstract: string,
    top_k: number
) => {

    const { data } = await client.post(
        "/ml/recommendation",
        {
            title,
            abstract,
            top_k,
        }
    );

    return data;
};