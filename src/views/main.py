import streamlit as st
import pandas as pd
from src.database.connection import get_connection, get_cursor, close_connection
from src.database.queries import (
    get_properties_query,
    get_final_preview_query,
    update_coordinates_query
)
from src.utils.coordinate_formatter import format_coordinate

def reset_app():
    """Força um reset completo da aplicação"""
    st.query_params.clear()
    st.query_params.update({"reset": str(pd.Timestamp.now().timestamp())})
    st.query_params.clear()
    st.rerun()

def process_excel_data(df):
    """Processa os dados do arquivo Excel."""
    registros = []
    for idx, row in df.iterrows():
        codigo = str(row['Codigo_Propriedade']).strip()
        latitude = format_coordinate(row['Latitude'], ensure_zero_prefix=True)
        longitude = format_coordinate(row['Longitude'], ensure_zero_prefix=False)
        registros.append((codigo, latitude, longitude))
    return registros

def create_comparison_dataframe(preview_df, final_preview_df):
    """Cria DataFrame comparativo entre dados do Excel e do banco."""
    comparison_df = pd.merge(
        preview_df.rename(columns={
            'Latitude_Formatada': 'Nova_Latitude',
            'Longitude_Formatada': 'Nova_Longitude'
        }),
        final_preview_df.rename(columns={
            'latitude': 'Latitude_Atual',
            'longitude': 'Longitude_Atual'
        }),
        left_on='Codigo_Propriedade',
        right_on='codigo_propriedade',
        how='outer'
    )
    
    return comparison_df[[
        'Codigo_Propriedade',
        'Latitude_Atual',
        'Nova_Latitude',
        'Longitude_Atual',
        'Nova_Longitude'
    ]]

def highlight_changes(row):
    """Destaca as mudanças no DataFrame comparativo."""
    styles = [''] * len(row)
    if row['Latitude_Atual'] != row['Nova_Latitude']:
        styles[1] = 'background-color: rgba(255, 0, 0, 0.1)'
        styles[2] = 'background-color: rgba(0, 255, 0, 0.1)'
    if row['Longitude_Atual'] != row['Nova_Longitude']:
        styles[3] = 'background-color: rgba(255, 0, 0, 0.1)'
        styles[4] = 'background-color: rgba(0, 255, 0, 0.1)'
    return styles

def update_database(registros):
    """Atualiza o banco de dados com os novos registros."""
    conn = get_connection()
    cur = get_cursor(conn)
    
    try:
        for codigo, latitude, longitude in registros:
            cur.execute(update_coordinates_query(), (latitude, longitude, codigo))
        conn.commit()
        
        # Gerar preview final
        codigos = ", ".join(f"'{c}'" for c, _, _ in registros)
        final_df = pd.read_sql_query(get_final_preview_query(codigos), conn)
        
        return final_df
    finally:
        close_connection(conn, cur)

def main():
    st.set_page_config(page_title="Atualizador de Latitude/Longitude", layout="centered")
    st.title("🚀 Atualizador de Latitude/Longitude")

    # Inicialização do estado
    if 'stage' not in st.session_state:
        st.session_state.stage = 'upload'
    if 'show_success' not in st.session_state:
        st.session_state.show_success = False

    # Se acabou de fazer um update com sucesso
    if st.session_state.show_success:
        st.balloons()
        
        if 'final_preview_df' in st.session_state:
            st.write("📊 **Pré-visualização final após update:**")
            st.dataframe(st.session_state.final_preview_df)
            
        st.success("Banco de dados atualizado com sucesso! 🚀")

        if st.button("🔄 Fazer Nova Atualização"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            reset_app()
                
        st.stop()

    # Placeholders
    placeholder_info = st.empty()
    placeholder_table_comparison = st.empty()
    placeholder_registers_success = st.empty()

    # Estágio de upload
    if st.session_state.stage == 'upload':
        placeholder_info.write("Arraste e solte seu arquivo XLS abaixo para processar e visualizar as alterações antes de atualizar o banco de dados.")
        
        uploaded_file = st.file_uploader("Escolha um arquivo XLS", type=["xls", "xlsx"])
        
        if uploaded_file is not None:
            st.session_state.stage = 'process'
            st.session_state.current_file = uploaded_file
            st.rerun()

    # Estágio de processamento
    elif st.session_state.stage == 'process':
        try:
            df = pd.read_excel(st.session_state.current_file)
            registros = process_excel_data(df)
            
            placeholder_info.empty()

            # Mostrar pré-visualização dos dados formatados
            preview_df = pd.DataFrame(registros, columns=['Codigo_Propriedade', 'Latitude_Formatada', 'Longitude_Formatada'])
            
            # Buscar dados atuais do banco
            conn = get_connection()
            codigos = ", ".join(f"'{c}'" for c, _, _ in registros)
            final_preview_df = pd.read_sql_query(get_properties_query(codigos), conn)
            close_connection(conn)

            placeholder_info.write("🔄 **Comparação dos Dados: Arquivo XLS vs Banco de Dados**")
            
            comparison_df = create_comparison_dataframe(preview_df, final_preview_df)
            
            placeholder_table_comparison.dataframe(
                comparison_df.style.apply(highlight_changes, axis=1),
                use_container_width=True
            )
            
            placeholder_registers_success.success(f"{len(registros)} registros carregados e formatados.")

            # Botões de ação
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Atualizar Banco de Dados"):
                    try:
                        with st.spinner("Atualizando banco de dados..."):
                            final_df = update_database(registros)
                            st.session_state.final_preview_df = final_df
                            st.session_state.show_success = True
                            st.rerun()
                                    
                    except Exception as e:
                        st.error(f"Erro ao atualizar banco ou gerar preview: {e}")
            
            with col2:
                if st.button("🔙 Escolher Outro Arquivo"):
                    st.session_state.stage = 'upload'
                    if 'current_file' in st.session_state:
                        del st.session_state.current_file
                    st.rerun()
                    
        except Exception as e:
            st.error(f"Erro ao processar XLS: {e}")
            if st.button("🔙 Voltar", key="btn_error_back"):
                st.session_state.stage = 'upload'
                if 'current_file' in st.session_state:
                    del st.session_state.current_file
                st.rerun()

if __name__ == "__main__":
    main() 