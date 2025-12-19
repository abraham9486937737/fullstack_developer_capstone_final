const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3030;

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Load data from the data/ folder
const reviews_data = JSON.parse(fs.readFileSync("./data/reviews.json", "utf8"));
const dealerships_data = JSON.parse(fs.readFileSync("./data/dealerships.json", "utf8"));

// Connect to MongoDB (container name from docker-compose)
mongoose.connect("mongodb://mongo_db:27017/", { dbName: "dealershipsDB" });

const Reviews = require("./review");
const Dealerships = require("./dealership");

// Seed database on startup
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data.reviews);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data.dealerships);

    console.log("Database seeded successfully");
  } catch (error) {
    console.error("Error seeding database:", error);
  }
})();

// Home
app.get("/", (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get("/fetchReviews", async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

// Fetch reviews by dealer ID
app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const dealerId = Number(req.params.id);
    const documents = await Reviews.find({ dealership: dealerId });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

// Fetch all dealerships
app.get("/fetchDealers", async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealers" });
  }
});

// Fetch dealerships by state (accepts full name or abbreviation, case-insensitive)
app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const stateParam = req.params.state.trim();
    const regex = new RegExp(`^${stateParam}$`, "i"); // case-insensitive exact match

    const documents = await Dealerships.find({
      $or: [{ state: regex }, { st: regex }],
    });

    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealers by state" });
  }
});

// Fetch a single dealer by numeric ID
app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const dealerId = Number(req.params.id);
    const document = await Dealerships.findOne({ id: dealerId });

    if (!document) {
      return res.status(404).json({ error: "Dealer not found" });
    }

    res.json(document);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealer by id" });
  }
});

// Insert a new review
app.post("/insert_review", async (req, res) => {
  try {
    const data = req.body;
    const documents = await Reviews.find().sort({ id: -1 });
    const new_id = (documents[0]?.id || 0) + 1;

    const review = new Reviews({
      id: new_id,
      name: data.name,
      dealership: Number(data.dealership),
      review: data.review,
      purchase: Boolean(data.purchase),
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: Number(data.car_year),
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error inserting review" });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
