export async function POST(request) {
    const data = await request.json();

    console.log(data);

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze-code", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const json = await response.json();
            console.log(json);
            return new Response(JSON.stringify(json), {
                status: 200,
                headers: {
                    "Content-Type": "application/json",
                },
            });
        } else {
            const error = await response.text();
            console.error(error);
            return new Response(error, {
                status: response.status,
                headers: {
                    "Content-Type": "application/json",
                },
            });
        }
    } catch (error) {
        console.error(error);
        return new Response(error, {
            status: 500,
            headers: {
                "Content-Type": "application/json",
            },
        });
    }
}