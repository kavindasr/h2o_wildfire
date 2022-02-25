from h2o_wave import main, app, Q, ui, data

async def about(q:Q):
    q.page['about'] = ui.markdown_card(    
        box='predict',    
        title='',    
        content=open('markdowns/about.md').read()
    )
    await q.page.save()