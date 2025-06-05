import streamlit as st
import re
import psycopg2
import os
import pandas as pd
import textwrap

st.set_page_config(page_title="Atualizador de Latitude/Longitude", layout="wide")
st.title("🚀 Atualizador de Latitude/Longitude")
st.write("Arraste e solte seu arquivo XLS abaixo para processar e visualizar as alterações antes de atualizar o banco de dados.")

uploaded_file = st.file_uploader("Escolha um arquivo XLS", type=["xls", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        def format_coordinate(value, ensure_zero_prefix=False):
            digits = re.sub(r'\D', '', str(value))
            if len(digits) > 7:
                digits = digits[:7]
            elif len(digits) < 7:
                digits = digits.ljust(7, '0')
            if ensure_zero_prefix and not digits.startswith('0'):
                digits = '0' + digits[1:]
            return digits

        registros = []
        for idx, row in df.iterrows():
            codigo = str(row['Codigo_Propriedade']).strip()
            latitude = format_coordinate(row['Latitude'], ensure_zero_prefix=True)
            longitude = format_coordinate(row['Longitude'], ensure_zero_prefix=False)
            registros.append((codigo, latitude, longitude))

        st.success(f"{len(registros)} registros carregados e formatados.")

        # Mostrar pré-visualização dos dados formatados ANTES do update
        preview_df = pd.DataFrame(registros, columns=['Codigo_Propriedade', 'Latitude_Formatada', 'Longitude_Formatada'])

        # Conectar ao banco e pegar o preview real
        db_config = {
            'dbname': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'port': os.environ.get('DB_PORT', '5432')
        }
        conn = psycopg2.connect(**db_config)
        codigos = ", ".join(f"'{c}'" for c, _, _ in registros)
        sql_before_update = textwrap.dedent(f'''
            SELECT
                pro.nu_codigoanimal,
                ie.vl_latitude,
                ie.vl_longitude
            FROM
                agrocomum.inscricaoestadual ie
            JOIN
                agrocomum.propriedade pro
                ON pro.id_inscricaoestadual = ie.id_inscricaoestadual
            WHERE
                pro.nu_codigoanimal IN ({codigos});
        ''')
        before_preview_df = pd.read_sql_query(sql_before_update, conn)
        conn.close()

        # Mostrar as duas tabelas lado a lado na mesma seção
        st.write("🔍 **Pré-visualização dos dados antes do update:**")
        col1, col2 = st.columns(2)

        with col1:
            st.write("📝 **Dados do XLS formatados:**")
            st.dataframe(preview_df)

        with col2:
            st.write("📦 **Dados atuais no banco:**")
            before_preview_df.columns = ['Codigo_Propriedade', 'Latitude', 'Longitude']
            st.dataframe(before_preview_df)

        # Botão para atualizar
        if st.button("Atualizar Banco de Dados"):
            try:
                conn = psycopg2.connect(**db_config)
                cur = conn.cursor()

                # Executar o update
                for codigo, latitude, longitude in registros:
                    cur.execute("""
                        UPDATE agrocomum.inscricaoestadual ie
                        SET vl_latitude = %s, vl_longitude = %s
                        FROM agrocomum.propriedade pro
                        WHERE pro.nu_codigoanimal = %s
                          AND pro.id_inscricaoestadual = ie.id_inscricaoestadual;
                    """, (latitude, longitude, codigo))
                conn.commit()
                cur.close()

                st.success("Banco de dados atualizado com sucesso! 🚀")

                # Gerar e executar o SELECT para mostrar preview dos dados reais no banco após update
                conn = psycopg2.connect(**db_config)
                sql_after_update = textwrap.dedent(f'''
                    SELECT
                        p.nome,
                        ll.loc_no,
                        ie.no_fantasia,
                        pro.nu_codigoanimal,
                        ie.vl_latitude,
                        ie.vl_longitude
                    FROM
                        agrocomum.inscricaoestadual ie
                    JOIN
                        agrocomum.propriedade pro
                        ON pro.id_inscricaoestadual = ie.id_inscricaoestadual
                    JOIN
                        rh.pessoa p
                        ON p.id = ie.id_pessoa
                    JOIN
                        agrocomum.inscricaoestadual_endereco iee
                        ON iee.id_inscricaoestadual = ie.id_inscricaoestadual
                    JOIN
                        agrocomum.endereco e
                        ON e.id_endereco = iee.id_endereco
                    JOIN
                        dne.log_localidade ll
                        ON ll.loc_nu = e.id_localidade
                    WHERE
                        pro.nu_codigoanimal IN ({codigos});
                ''')
                final_preview_df = pd.read_sql_query(sql_after_update, conn)
                conn.close()

                st.write("📊 **Preview final após update:**")
                st.dataframe(final_preview_df)

            except Exception as e:
                st.error(f"Erro ao atualizar banco ou gerar preview: {e}")
    except Exception as e:
        st.error(f"Erro ao processar XLS: {e}")
