import streamlit as st
import pandas as pd
import time
import sys
import os

# Add the current directory to path if needed
if '.' not in sys.path:
    sys.path.append('.')

# Import the predictor
try:
    from rice_yield_predictor import RiceYieldPredictor
    predictor_available = True
except Exception as e:
    predictor_available = False
    predictor_error = str(e)

# Streamlit UI Setup
st.set_page_config(page_title="Rice Yield Prediction", page_icon="🌾", layout="centered")
# --- Custom CSS ---
def local_css():
    st.markdown("""
        <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #1c1c1c;
        }
        .main {
            padding: 2rem;
        }
        h1 {
            font-weight: 700;
            margin-bottom: 20px;
        }
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            background: linear-gradient(to right, #4CAF50, #81C784);
            color: white;
            height: 2.8em;
            font-size: 17px;
            margin-top: 8px;
            border: none;
        }
        .stButton > button:hover {
            background: linear-gradient(to right, #388E3C, #66BB6A);
        }
        .card {
            background: rgba(255, 255, 255, 0.05);
            padding: 0.6rem 1.2rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            width: 90%;
            margin: auto;
        }
        /* Light theme - lighter shadow */
        body[data-theme='light'] .card {
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1); /* Lighter shadow for light mode */
        }

        /* Dark theme - bright white shadow */
        body[data-theme='dark'] .card {
            box-shadow: 0 12px 30px rgba(255, 255, 255, 0.2); /* Slightly bright shadow for dark mode */
        }

        /* Hover effect */
        .card:hover {
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
        }

        body[data-theme='light'] .card:hover {
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.2); /* Lighter hover shadow */
        }

        body[data-theme='dark'] .card:hover {
            box-shadow: 0 16px 40px rgba(255, 255, 255, 0.3); /* White hover shadow */
        }
        .sidebar-content {
            font-size: 15px;
            color: #ddd;
        }
        hr {
            border: none;
            border-top: 1px solid #444;
            margin: 1.2rem 0;
        }
        .error-message {
            color: #ff6b6b;
            background-color: rgba(255, 107, 107, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .info-message {
            color: #4dabf7;
            background-color: rgba(77, 171, 247, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

def card_start():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

# --- Apply CSS ---
local_css()

# Initialize predictor
@st.cache_resource
def load_predictor():
    try:
        return RiceYieldPredictor(), None
    except Exception as e:
        return None, str(e)

# Load the predictor (will be cached)
predictor, load_error = load_predictor()

# --- Sidebar with Manual and Dummy Data ---
with st.sidebar:
    st.markdown("## 📖 User Manual")
    st.markdown(
        """
        1. **Select Region** - Choose the area of cultivation.  
        2. **Select Rice Type** - Choose the rice variety.  
        3. **Enter Area Size** - In hectares.  
        4. Click **Predict** to see results.
        5. Click **Reset** to start over.
        """
    )
    st.markdown("---")
    st.markdown("## 📊 Sample Data")
    sample_df = pd.DataFrame({
        "Region": ["Barishal", "Dhaka", "Sylhet"],
        "Rice Type": ["Amon HYV", "Boro HYV", "Aus Local"],
        "Area (ha)": [2.5, 4.0, 3.2],
        "Yield/ha (tons)": [5.2, 6.8, 4.1],
        "Total Yield (tons)": [13.0, 27.2, 13.12]
    })
    st.dataframe(sample_df)
    
    # Display model info
    st.markdown("---")
    st.markdown("## 🧠 Model Information")
    if predictor:
        st.markdown("✅ **ML Model loaded successfully**")
        st.markdown(f"- **Regions available**: {len(predictor.get_regions())}")
        st.markdown(f"- **Rice types available**: {len(predictor.get_rice_types())}")
    else:
        st.markdown(f"❌ **Error loading model**: {load_error}")

# --- Main Title ---
st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌾 Rice Yield Prediction 🌾</h1>", unsafe_allow_html=True)

# --- Main Form ---
with st.container():
    card_start()
    st.subheader("", divider='rainbow')
    st.markdown("<h3 style='text-align: center;'>📅 Input Details</h3>", unsafe_allow_html=True)

    # Get regions and rice types from the model if available
    if predictor:
        regions = predictor.get_regions()
        rice_types = predictor.get_rice_types()
    else:
        # Fallback to the original lists
        regions = ["Barishal", "Bhola", "Patuakhali", "Chandpur", "Chattogram", "Cumilla", "Cox' Bazar", "Feni", "Noakhali", "Rangamati",
                "Dhaka", "Faridpur", "Madaripur", "Tangail", "Bagerhat", "Chuadanga", "Jashore", "Khulna", "Satkhira", "Mymensingh",
                "Bogura", "Pabna", "Rajshahi", "Dinajpur", "Nilphamari", "Rangpur", "Hobigonj", "Sylhet"]
        rice_types = ["Amon Broadcast", "Amon HYV", "Amon L.T", "Aus HYV", "Aus Local", "Boro HYV", "Boro Hybrid", "Boro Local"]
        
        # Show model error if applicable
        if load_error:
            st.markdown(f"""
                <div class="error-message">
                ⚠️ Model could not be loaded: {load_error}<br>
                Falling back to demo mode with random predictions.
                </div>
            """, unsafe_allow_html=True)

    region = st.selectbox("🌍 Select Region", regions, index=None, placeholder="None")
    rice_type = st.selectbox("🌾 Select Rice Type", rice_types, index=None, placeholder="None")
    area_size = st.number_input("📏 Enter Area Size (in hectares)", value=None, placeholder="0.0", step=0.1)

    if "predict_clicked" not in st.session_state:
        st.session_state.predict_clicked = False

    col1, col2 = st.columns(2)

    with col1:
        predict_button = st.button("🚀 Predict")
        if predict_button:
            if region and rice_type and area_size:
                st.session_state.predict_clicked = True
            else:
                st.warning("⚠️ Please fill in all fields before predicting!")

    with col2:
        if st.button("🔁 Reset"):
            st.session_state.predict_clicked = False
            st.rerun()

    # --- Prediction Output ---
    if st.session_state.predict_clicked:
        with st.spinner("🔄 Predicting rice yield..."):
            time.sleep(1)  # Simulate processing time
            
            # Use the model for prediction if available
            if predictor and predictor_available:
                try:
                    prediction = predictor.predict(region, rice_type, area_size)
                    if 'error' in prediction:
                        st.error(f"Prediction error: {prediction['error']}")
                        # Fall back to random values
                        import random
                        yield_per_hectare = round(random.uniform(3.5, 8.5), 2)
                        total_yield = round(yield_per_hectare * area_size, 2)
                        st.markdown("""
                            <div class="info-message">
                            ℹ️ Falling back to demo mode with random prediction.
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        yield_per_hectare = prediction['yield_per_hectare']
                        total_yield = prediction['total_yield']
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    # Fall back to random values
                    import random
                    yield_per_hectare = round(random.uniform(3.5, 8.5), 2)
                    total_yield = round(yield_per_hectare * area_size, 2)
                    st.markdown("""
                        <div class="info-message">
                        ℹ️ Falling back to demo mode with random prediction.
                        </div>
                    """, unsafe_allow_html=True)
            else:
                # Fall back to random values as in the original code
                import random
                yield_per_hectare = round(random.uniform(3.5, 8.5), 2)
                total_yield = round(yield_per_hectare * area_size, 2)
                
                if not predictor_available:
                    st.markdown("""
                        <div class="info-message">
                        ℹ️ Using demo mode with random prediction (model not available).
                        </div>
                    """, unsafe_allow_html=True)

            st.success(f"✅ **Prediction Complete!**")
            st.markdown(f"""
                <div style="font-size: 16px; padding: 1rem; border-radius: 10px; background-color: #1e1e1e; color: #d1ffd6;">
                    <strong>🌍 Region:</strong> {region} <br>
                    <strong>🌾 Rice Type:</strong> {rice_type} <br>
                    <strong>📏 Area:</strong> {area_size} hectares <br>
                    <hr>
                    <strong>📈 Estimated Yield per hectare:</strong> <span style="color:#4caf50;">{yield_per_hectare} tons</span><br>
                    <strong>📊 Total Estimated Yield:</strong> <span style="color:#66bb6a;">{total_yield} tons</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.subheader("", divider='rainbow')
    card_end()

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>©️ 2025 - Rice Yield Prediction System</p>", unsafe_allow_html=True)