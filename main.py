from fastapi import FastAPI
import uvicorn
from utils.get_data import get_data, stats_data
from utils.get_visuals import rating_distributions, review_table
from utils.insight_generation import create_insights, commonn_words
from fastapi.responses import StreamingResponse, HTMLResponse
import json
from io import BytesIO

data = get_data()
stats = stats_data(data)
insights = create_insights(data)
common_review, common_phrases_review, wordcloud_review = commonn_words(insights['insights_data'], 'review')
common_title, common_phrases_title, wordcloud_title = commonn_words(insights['insights_data'], 'title')

app = FastAPI()

@app.get('/rating')
def get_chart():

    html_content = f""" <h1>3. Basic Metrics:</h1>
    <h2>Average rating in selected reviews = {stats['mean']}</h2>
                    {rating_distributions(data)}
 <h1>4. Insights:</h1>
 Accuracy by review type = {insights['accuracy_review']} 
 <br>
 Accuracy by title type = {insights['accuracy_title']} 
 <br>
 <br>
 Common 10 words in review = {common_review}
 <br>
 Top 10 Important Phrases in Review (TF-IDF):  {common_phrases_review}
 <br>
  <h2>Word Cloud from review</h2>
            <img src="data:image/png;base64,{wordcloud_review}" alt="Word Cloud">
 <br>
 <br>
 Common 10 words in tittle = {common_title}
<br>
 Top 10 Important Phrases in Title (TF-IDF):  {common_phrases_title}
 
 <h2>Word Cloud from title</h2>
            <img src="data:image/png;base64,{wordcloud_title}" alt="Word Cloud">
"""

    return HTMLResponse(content=html_content)


@app.get('/table')
def get_chart():

    html_content = review_table(data)

    return HTMLResponse(content=html_content)


@app.get("/download_json")
def download_json():
    # Sample JSON data
    data_json = data.to_json(orient="records", indent=4)

    # Convert dict to JSON string and encode it
    json_str = json.dumps(data_json, indent=4)
    json_bytes = BytesIO(json_str.encode("utf-8"))

    # Serve as a downloadable file
    return StreamingResponse(json_bytes, media_type="application/json", headers={
        "Content-Disposition": "attachment; filename=data.json"
    })

# (app_name: str='nebula-horoscope-astrology', app_id: str='1459969523')
@app.get("/update/")
def update_data(app_name: str='nebula-horoscope-astrology', app_id: str='1459969523'):
    global data
    data = get_data(app_name, app_id)
    global stats
    stats = stats_data(data)
    global insights
    insights = create_insights(data)
    global common_review, common_phrases_review, wordcloud_review
    common_review, common_phrases_review, wordcloud_review  = commonn_words(insights['insights_data'], 'review')
    global common_title, common_phrases_title, wordcloud_title
    common_title, common_phrases_title, wordcloud_title = commonn_words(insights['insights_data'], 'title')

    html_content = f""" <h1>New App Selected</h1>
    """

    return HTMLResponse(content=html_content)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0",  reload=True)