import textwrap

def get_properties_query(codigos):
    """Retorna query para buscar propriedades pelos códigos."""
    return textwrap.dedent(f'''
        SELECT
            pro.nu_codigoanimal as codigo_propriedade,
            ie.vl_latitude as latitude,
            ie.vl_longitude as longitude
        FROM
            agrocomum.inscricaoestadual ie
        JOIN
            agrocomum.propriedade pro
            ON pro.id_inscricaoestadual = ie.id_inscricaoestadual
        WHERE
            pro.nu_codigoanimal IN ({codigos});
    ''')

def get_final_preview_query(codigos):
    """Retorna query para preview final após atualização."""
    return textwrap.dedent(f'''
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

def update_coordinates_query():
    """Retorna query para atualizar coordenadas."""
    return """
        UPDATE agrocomum.inscricaoestadual ie
        SET vl_latitude = %s, vl_longitude = %s
        FROM agrocomum.propriedade pro
        WHERE pro.nu_codigoanimal = %s
          AND pro.id_inscricaoestadual = ie.id_inscricaoestadual;
    """ 