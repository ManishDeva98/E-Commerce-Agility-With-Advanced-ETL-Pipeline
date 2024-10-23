def MyTransform (glueContext, dfc) -> DynamicFrameCollection:
    df1 = dfc.select(list(dfc.keys())[0]).toDF()
    df2 = dfc.select(list(dfc.keys())[1]).toDF()
    
    for col_name in df1.columns:
        sanitized_name = col_name.replace(" ", "_")
        df1 = df1.withColumnRenamed(col_name, sanitized_name)
        
    for col_name in df2.columns:
        sanitized_name = col_name.replace(" ", "_")
        df2 = df2.withColumnRenamed(col_name, sanitized_name)
    
    df1_cleaned = df1.dropna()
    df2_cleaned = df2.dropna()
    
    df1_unique = df1_cleaned.dropDuplicates()
    df2_unique = df2_cleaned.dropDuplicates()
    
    # Perform the join operation
    df_joined = df1_unique.join(df2_unique, on='Order_ID', how='outer')
    
    # Coalesce to a single partition to produce a single file
    df_joined_single_file = df_joined.coalesce(1)
    
    # Convert back to DynamicFrame
    dynamic_frame_joined = DynamicFrame.fromDF(df_joined_single_file, glueContext, "joined_data")
    
    # Write the output as a single CSV file to S3
    
    return DynamicFrameCollection({"joined_data": dynamic_frame_joined}, glueContext)