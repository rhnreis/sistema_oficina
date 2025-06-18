from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

def gerar_pdf_orcamento(orcamento):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    
    # Título
    elements.append(Paragraph("Orçamento de Serviço", styles["h1"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Informações do Cliente
    elements.append(Paragraph("**Cliente:** " + orcamento.cliente.nome, styles["Normal"]))
    elements.append(Paragraph("**CPF/CNPJ:** " + orcamento.cliente.cpf_cnpj, styles["Normal"]))
    elements.append(Paragraph("**Telefone:** " + orcamento.cliente.telefone, styles["Normal"]))
    elements.append(Paragraph("**Email:** " + orcamento.cliente.email, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Informações do Orçamento
    elements.append(Paragraph("**Número do Orçamento:** " + orcamento.numero_orcamento, styles["Normal"]))
    elements.append(Paragraph("**Data de Criação:** " + orcamento.data_criacao.strftime("%d/%m/%Y"), styles["Normal"]))
    elements.append(Paragraph("**Status:** " + orcamento.status.capitalize(), styles["Normal"]))
    elements.append(Paragraph("**Descrição do Serviço:** " + orcamento.descricao_servico, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Itens do Orçamento
    data = [["Descrição", "Quantidade", "Valor Unitário", "Total"]] # Cabeçalho da tabela
    for item in orcamento.itens:
        data.append([
            item.material.nome if item.material else item.descricao,
            str(item.quantidade),
            f"R$ {item.preco_unitario:.2f}",
            f"R$ {item.total_item:.2f}"
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2 * 72))
    
    # Totais
    elements.append(Paragraph(f"**Valor Mão de Obra:** R$ {orcamento.valor_mao_obra:.2f}", styles["Normal"], alignment=TA_RIGHT))
    elements.append(Paragraph(f"**Total do Orçamento:** R$ {orcamento.valor_total:.2f}", styles["h2"], alignment=TA_RIGHT))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Observações
    if orcamento.observacoes:
        elements.append(Paragraph("**Observações:**", styles["h3"]))
        elements.append(Paragraph(orcamento.observacoes, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * 72))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def gerar_pdf_ordem_servico(ordem_servico):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    
    # Título
    elements.append(Paragraph("Ordem de Serviço", styles["h1"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Informações da Ordem de Serviço
    elements.append(Paragraph("**Número da OS:** " + ordem_servico.numero_ordem, styles["Normal"]))
    elements.append(Paragraph("**Data de Criação:** " + ordem_servico.data_criacao.strftime("%d/%m/%Y"), styles["Normal"]))
    elements.append(Paragraph("**Status:** " + ordem_servico.status.capitalize(), styles["Normal"]))
    elements.append(Paragraph("**Cliente:** " + ordem_servico.orcamento.cliente.nome, styles["Normal"]))
    elements.append(Paragraph("**Orçamento Relacionado:** " + ordem_servico.orcamento.numero_orcamento, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Descrição do Serviço
    elements.append(Paragraph("**Descrição do Serviço:**", styles["h3"]))
    elements.append(Paragraph(ordem_servico.orcamento.descricao_servico, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Itens do Orçamento (da OS)
    data = [["Descrição", "Quantidade", "Valor Unitário", "Total"]] # Cabeçalho da tabela
    for item in ordem_servico.orcamento.itens:
        data.append([
            item.material.nome if item.material else item.descricao,
            str(item.quantidade),
            f"R$ {item.preco_unitario:.2f}",
            f"R$ {item.total_item:.2f}"
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2 * 72))
    
    # Totais
    elements.append(Paragraph(f"**Valor Mão de Obra:** R$ {ordem_servico.orcamento.valor_mao_obra:.2f}", styles["Normal"], alignment=TA_RIGHT))
    elements.append(Paragraph(f"**Total da OS:** R$ {ordem_servico.orcamento.valor_total:.2f}", styles["h2"], alignment=TA_RIGHT))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Observações
    if ordem_servico.observacoes:
        elements.append(Paragraph("**Observações:**", styles["h3"]))
        elements.append(Paragraph(ordem_servico.observacoes, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * 72))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def gerar_pdf_contrato(contrato):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    
    # Título
    elements.append(Paragraph("Contrato de Prestação de Serviços", styles["h1"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Informações do Contrato
    elements.append(Paragraph("**Número do Contrato:** " + contrato.numero_contrato, styles["Normal"]))
    elements.append(Paragraph("**Data de Criação:** " + contrato.data_criacao.strftime("%d/%m/%Y"), styles["Normal"]))
    elements.append(Paragraph("**Status:** " + contrato.status.capitalize(), styles["Normal"]))
    elements.append(Paragraph("**Cliente:** " + contrato.ordem_servico.orcamento.cliente.nome, styles["Normal"]))
    elements.append(Paragraph("**Ordem de Serviço Relacionada:** " + contrato.ordem_servico.numero_ordem, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Termos e Condições
    elements.append(Paragraph("**Termos e Condições:**", styles["h3"]))
    elements.append(Paragraph(contrato.termos_condicoes, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def gerar_pdf_nota_fiscal(nota_fiscal):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    
    # Título
    elements.append(Paragraph("Nota Fiscal de Serviço", styles["h1"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Informações da Nota Fiscal
    elements.append(Paragraph("**Número da NF:** " + nota_fiscal.numero_nf, styles["Normal"]))
    elements.append(Paragraph("**Data de Emissão:** " + nota_fiscal.data_emissao.strftime("%d/%m/%Y"), styles["Normal"]))
    elements.append(Paragraph("**Status:** " + nota_fiscal.status.capitalize(), styles["Normal"]))
    elements.append(Paragraph("**Cliente:** " + nota_fiscal.ordem_servico.orcamento.cliente.nome, styles["Normal"]))
    elements.append(Paragraph("**Ordem de Serviço Relacionada:** " + nota_fiscal.ordem_servico.numero_ordem, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Detalhes do Serviço
    elements.append(Paragraph("**Descrição do Serviço:**", styles["h3"]))
    elements.append(Paragraph(nota_fiscal.ordem_servico.orcamento.descricao_servico, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Totais
    elements.append(Paragraph(f"**Valor Total da NF:** R$ {nota_fiscal.valor_total:.2f}", styles["h2"], alignment=TA_RIGHT))
    elements.append(Spacer(1, 0.2 * 72))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def gerar_pdf_relatorio_servicos(ordens, filtros):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    
    # Título
    elements.append(Paragraph("Relatório de Serviços", styles["h1"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Filtros Aplicados
    elements.append(Paragraph("**Filtros Aplicados:**", styles["h3"]))
    if filtros.get("data_inicio"):
        elements.append(Paragraph(f"Data Início: {filtros["data_inicio"]}", styles["Normal"]))
    if filtros.get("data_fim"):
        elements.append(Paragraph(f"Data Fim: {filtros["data_fim"]}", styles["Normal"]))
    if filtros.get("cliente_id"):
        # Você precisaria buscar o nome do cliente aqui se quiser exibir o nome em vez do ID
        elements.append(Paragraph(f"Cliente ID: {filtros["cliente_id"]}", styles["Normal"]))
    if filtros.get("status"):
        elements.append(Paragraph(f"Status: {filtros["status"].capitalize()}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * 72))
    
    # Tabela de Serviços
    data = [["OS", "Cliente", "Orçamento", "Data Início", "Data Conclusão", "Status", "Valor Total"]] # Cabeçalho
    for ordem in ordens:
        data.append([
            ordem.numero_ordem,
            ordem.orcamento.cliente.nome,
            ordem.orcamento.numero_orcamento,
            ordem.data_inicio.strftime("%d/%m/%Y"),
            ordem.data_conclusao.strftime("%d/%m/%Y") if ordem.data_conclusao else "-",
            ordem.status.capitalize(),
            f"R$ {ordem.orcamento.valor_total:.2f}"
        ])
        
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2 * 72))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

