"""
Module pour l'affichage du sélecteur de date style mobile 
avec intégration du module de temps centralisé
"""

import streamlit as st
from datetime import datetime, timedelta
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_enhanced_date_selector(data_hub, days_count=7):
    """
    Génère un sélecteur de date horizontal style mobile avec le module temps
    
    Args:
        data_hub: Instance du hub d'intégration central avec module temps
        days_count: Nombre de jours à afficher
    """
    try:
        # Obtenir les jours formatés via le module de temps
        upcoming_days = data_hub.get_upcoming_days_formatted(days_count)
        
        # CSS pour le sélecteur de date
        st.markdown("""
        <style>
        .date-selector {
            display: flex;
            overflow-x: auto;
            padding: 10px 0;
            margin-bottom: 20px;
            -webkit-overflow-scrolling: touch;
        }
        .date-item {
            min-width: 70px;
            height: 70px;
            margin-right: 12px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #2D2D44;
            border-radius: 10px;
            padding: 5px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 2px solid transparent;
        }
        .date-item.selected {
            background-color: #7038FF;
            border: 2px solid #9969FF;
            box-shadow: 0px 0px 10px rgba(122, 56, 255, 0.5);
        }
        .date-item:hover {
            background-color: #3D3D64;
        }
        .date-day {
            font-size: 12px;
            color: #BBBBCC;
            margin-bottom: 5px;
        }
        .date-date {
            font-size: 18px;
            font-weight: bold;
        }
        .weekend {
            background-color: #383850;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Générer le HTML pour le sélecteur de date
        date_selector_html = '<div class="date-selector">'
        
        for i, day in enumerate(upcoming_days):
            date_obj = datetime.fromisoformat(day['date'])
            is_selected = date_obj.date() == st.session_state.selected_date
            is_weekend = day['is_weekend']
            
            # Créer la classe CSS appropriée
            css_class = "date-item"
            if is_selected:
                css_class += " selected"
            if is_weekend:
                css_class += " weekend"
                
            date_selector_html += f"""
            <div class="{css_class}" id="date_{i}" onclick="selectDate({i})">
                <div class="date-day">{day['display_name']}</div>
                <div class="date-date">{day['formatted_date']}</div>
            </div>
            """
        
        date_selector_html += '</div>'
        
        # Ajouter le code JavaScript pour la gestion des clics
        date_selector_html += """
        <script>
        function selectDate(index) {
            // Envoyer l'indice de la date sélectionnée au backend Streamlit
            const data = {
                index: index,
                date: new Date().toISOString()  // Ajouter une date pour forcer la mise à jour
            };
            
            // Utiliser l'API Streamlit pour communiquer
            if (window.Streamlit) {
                window.Streamlit.setComponentValue(data);
            }
        }
        </script>
        """
        
        # Afficher le sélecteur
        st.markdown(date_selector_html, unsafe_allow_html=True)
        
        # Contrôleur de date caché pour gérer les changements
        date_change = st.radio(
            "Sélectionner une date",
            options=range(len(upcoming_days)),
            index=0,
            key="date_radio",
            label_visibility="collapsed"
        )
        
        # Mettre à jour la date sélectionnée
        if date_change is not None:
            selected_date = datetime.fromisoformat(upcoming_days[date_change]['date']).date()
            if selected_date != st.session_state.selected_date:
                st.session_state.selected_date = selected_date
                logger.info(f"Date sélectionnée modifiée: {selected_date}")
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération du sélecteur de date amélioré: {e}")
        # Fallback au sélecteur standard
        generate_standard_date_selector(days_count)

def generate_standard_date_selector(days_count=7):
    """
    Génère un sélecteur de date standard au cas où le module temps n'est pas disponible
    
    Args:
        days_count: Nombre de jours à afficher
    """
    # CSS pour le sélecteur de date
    st.markdown("""
    <style>
    .date-selector {
        display: flex;
        overflow-x: auto;
        padding: 10px 0;
        margin-bottom: 20px;
        -webkit-overflow-scrolling: touch;
    }
    .date-item {
        min-width: 70px;
        height: 70px;
        margin-right: 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #2D2D44;
        border-radius: 10px;
        padding: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .date-item.selected {
        background-color: #7038FF;
        box-shadow: 0px 0px 10px rgba(122, 56, 255, 0.5);
    }
    .date-item:hover {
        background-color: #3D3D64;
    }
    .date-day {
        font-size: 12px;
        color: #BBBBCC;
        margin-bottom: 5px;
    }
    .date-date {
        font-size: 18px;
        font-weight: bold;
    }
    .weekend {
        background-color: #383850;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Générer les dates
    today = datetime.now().date()
    dates = [today + timedelta(days=i) for i in range(days_count)]
    
    # Créer les options pour le sélecteur
    date_options = []
    for date in dates:
        # Déterminer si c'est un jour de week-end
        is_weekend = date.weekday() >= 5
        
        # Déterminer le nom du jour
        if date == today:
            day_name = "Aujourd'hui"
        elif date == today + timedelta(days=1):
            day_name = "Demain"
        else:
            days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            day_name = days[date.weekday()][:3]
        
        date_options.append({
            "date": date,
            "day_name": day_name,
            "is_weekend": is_weekend
        })
    
    # Générer le HTML pour le sélecteur de date
    date_selector_html = '<div class="date-selector">'
    
    for i, option in enumerate(date_options):
        date = option["date"]
        is_selected = date == st.session_state.selected_date
        is_weekend = option["is_weekend"]
        
        # Créer la classe CSS appropriée
        css_class = "date-item"
        if is_selected:
            css_class += " selected"
        if is_weekend:
            css_class += " weekend"
            
        date_selector_html += f"""
        <div class="{css_class}" onclick="document.getElementById('date_{i}').click()">
            <div class="date-day">{option['day_name']}</div>
            <div class="date-date">{date.day}/{date.month}</div>
        </div>
        """
    
    date_selector_html += '</div>'
    
    # Afficher le sélecteur
    st.markdown(date_selector_html, unsafe_allow_html=True)
    
    # Contrôleur de date caché pour gérer les changements
    selected_index = next((i for i, o in enumerate(date_options) if o["date"] == st.session_state.selected_date), 0)
    date_change = st.radio(
        "Sélectionner une date",
        options=range(len(date_options)),
        index=selected_index,
        key="date_radio_standard",
        label_visibility="collapsed"
    )
    
    # Mettre à jour la date sélectionnée
    if date_change is not None:
        selected_date = date_options[date_change]["date"]
        if selected_date != st.session_state.selected_date:
            st.session_state.selected_date = selected_date