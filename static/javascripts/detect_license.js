const input = document.getElementById("uploadInput");
input.addEventListener("change", async (event) => {
    handle_data(event.target.files[0]);
})

async function handle_data(file) {
    const data = new FormData();
    data.append("image_file", file, "image_file");
    document.getElementById("title_image").innerText = "Handling..."
    const response = await fetch("/detect-license-plate", {
        method: "post",
        body: data
    });
    const boxes = await response.json();
    draw_image_and_boxes(file, boxes);
}

function draw_image_and_boxes(file, boxes) {
    const img = new Image()
    img.src = URL.createObjectURL(file);
    img.onload = () => {
        document.getElementById("title_image").innerText = "Please check result: Detect " + boxes.length + " result."
        const canvas = document.querySelector("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        ctx.strokeStyle = "#00FF00";
        ctx.lineWidth = 3;
        ctx.font = "18px serif";
        boxes.forEach(([x1, y1, x2, y2, prob, number_license]) => {
            ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
            ctx.fillStyle = "#00ff00";
            text = prob +":::" + number_license;
            const width = ctx.measureText(text).width;
            ctx.fillRect(x1, y2, width + 10, 25);
            ctx.fillStyle = "#000000";
            ctx.fillText(text, x1, y2+18)
        });
    }
}