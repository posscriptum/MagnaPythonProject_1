def mysqlquery(data0, data1, data2,
                data3, data4, data5, data6, data7, data8):

    import pypyodbc
    conn = pypyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                             'Database=press_data_control;'
                             'uid=press_spvz; '
                             'pwd=admin100;')

    cursor = conn.cursor()



    SQLquery = (""" 
                    INSERT INTO pressAIDA1000(UserID,UserLogin,SlideHeightPreset,
                    SlideHeightActual,SensSumState,spmPreset,spmActual,CushionPressurePreset,CushionPressureActual) 
                    VALUES (?,?,?,?,?,?,?,?,?)      
                """)
    values = (data0, data1, data2, data3,
             data4, data5, data6, data7,
             data8)

    cursor.execute(SQLquery, values)
     # results = cursor.fetchall()

     # print(results)
    conn.commit()
    conn.close()