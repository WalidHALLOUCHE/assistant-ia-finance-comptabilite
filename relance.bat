@echo off
echo ==========================================
echo  🔄 RELANCE ET TEST DU PROJET AI DAF
echo ==========================================

echo.
echo [1/5] Verification de la configuration...
python verify_setup.py

echo.
echo [2/5] Generation des nouvelles donnees...
python scripts/generate_demo_data.py

echo.
echo [3/5] Construction de la base vectorielle (RAG)...
python scripts/build_vector_store.py

echo.
echo [4/5] Execution des tests unitaires...
pytest tests/ -v

echo.
echo [5/5] Lancement de l'application Streamlit...
streamlit run app.py