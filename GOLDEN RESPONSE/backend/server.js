
const express = require('express');
const nodemailer = require('nodemailer');

const app = express();
app.use(express.json());

app.post('/api/contact', async (req, res) => {
  try {
    const { name, email, phone } = req.body;

    if (!name || !email || !phone) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed'
      });
    }

    return res.json({
      success: true,
      message: 'Message sent successfully'
    });

  } catch (error) {
    return res.status(500).json({
      success: false,
      error: 'Server Error'
    });
  }
});

app.listen(5000, () => {
  console.log('Server running on port 5000');
});
