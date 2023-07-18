const list_dect = {
    0: 'person',
    1: 'bicycle',
    2: 'car',
    3: 'motorcycle',
    4: 'airplane',
    5: 'bus',
    6: 'train',
    7: 'truck',
    8: 'boat',
    9: 'traffic light',
    10: 'fire hydrant',
    11: 'stop sign',
    12: 'parking meter',
    13: 'bench',
    14: 'bird',
    15: 'cat',
    16: 'dog',
    17: 'horse',
    18: 'sheep',
    19: 'cow',
    20: 'elephant',
    21: 'bear',
    22: 'zebra',
    23: 'giraffe',
    24: 'backpack',
    25: 'umbrella',
    26: 'handbag',
    27: 'tie',
    28: 'suitcase',
    29: 'frisbee',
    30: 'skis',
    31: 'snowboard',
    32: 'sports ball',
    33: 'kite',
    34: 'baseball bat',
    35: 'baseball glove',
    36: 'skateboard',
    37: 'surfboard',
    38: 'tennis racket',
    39: 'bottle',
    40: 'wine glass',
    41: 'cup',
    42: 'fork',
    43: 'knife',
    44: 'spoon',
    45: 'bowl',
    46: 'banana',
    47: 'apple',
    48: 'sandwich',
    49: 'orange',
    50: 'broccoli',
    51: 'carrot',
    52: 'hot dog',
    53: 'pizza',
    54: 'donut',
    55: 'cake',
    56: 'chair',
    57: 'couch',
    58: 'potted plant',
    59: 'bed',
    60: 'dining table',
    61: 'toilet',
    62: 'tv',
    63: 'laptop',
    64: 'mouse',
    65: 'remote',
    66: 'keyboard',
    67: 'cell phone',
    68: 'microwave',
    69: 'oven',
    70: 'toaster',
    71: 'sink',
    72: 'refrigerator',
    73: 'book',
    74: 'clock',
    75: 'vase',
    76: 'scissors',
    77: 'teddy bear',
    78: 'hair drier',
    79: 'toothbrush'
};
const select_type = document.getElementById("type_detect");
for (const [key, value] of Object.entries(list_dect)) {
    var option = document.createElement("option");
    option.text = value.charAt(0).toUpperCase() + value.slice(1);
    option.value = key;
    select_type.appendChild(option)
}

const input = document.getElementById("uploadInput");
input.addEventListener("change", async (event) => {
    // const file = event.target.files[0];
    // const data = new FormData();
    // data.append("image_file", file, "image_file");
    // console.log(select_type.value);
    // data.append("type_detect", select_type.value);
    // document.getElementById("title_image").innerText = "Handling..."
    // const response = await fetch("/detect", {
    //     method: "post",
    //     body: data
    // });
    // const boxes = await response.json();
    // draw_image_and_boxes(file, boxes);
    handle_data(event.target.files[0]);
})

select_type.addEventListener("change",async ()=>{
    console.log("Change value: "+ select_type.value);
    let file = input.files[0]
    if(file != null)
    {
         handle_data(file);
    }
});

async function handle_data(file)
{
    const data = new FormData();
    data.append("image_file", file, "image_file");
    console.log(select_type.value);
    data.append("type_detect", select_type.value);
    document.getElementById("title_image").innerText = "Handling..."
    const response = await fetch("/detect", {
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
        // img.width = img.width > max_width ? max_width : img.width;
        // img.height = img.height > max_height ? max_height : img.height;
        document.getElementById("title_image").innerText = "Please check result: Detect "+ boxes.length + " result."
        const canvas = document.querySelector("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        ctx.strokeStyle = "#00FF00";
        ctx.lineWidth = 3;
        ctx.font = "18px serif";
        boxes.forEach(([x1, y1, x2, y2, label]) => {
            ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
            // ctx.fillStyle = "#00ff00";
            // const width = ctx.measureText(label).width;
            // ctx.fillRect(x1, y1, width + 10, 25);
            // ctx.fillStyle = "#000000";
            // ctx.fillText(label, x1, y1 + 18);
        });
    }
}