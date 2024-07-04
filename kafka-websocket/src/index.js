import express from "express";

const app = express();

const PORT = 8000;



app.listen(PORT, async () => {
    console.log(`Listiening to port ----> ${PORT}`);
});