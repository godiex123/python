materiales = """
                    SELECT 
                        -- "CONTINUIDAD" Aula,
                        IFNULL(n.idnumber, "") idnumber, 
                        IFNULL(n.Facultad, "") Facultad, 
                        IFNULL(n.Escuela, "") Escuela, 
                        IFNULL(n.Programa, "") Programa,
                        IFNULL(n.fullname, "")  Curso, 
                        IFNULL(n.shortname, "")  seccion_curso, 
                        IFNULL(n.Creacion, "") Creacion, 
                        IFNULL(n.Inicio, "") Inicio,
                        IFNULL(n.Docentes, "") Docentes, 
                        IFNULL(n.nd,0) "cantidad_docentes", 
                        IFNULL(z.mrec,0) Tot_Recursos, 
                        IFNULL(z.mact,0) Tot_Actividades, 
                        IFNULL(z.orec,0) Otros_Recursos, 
                        IFNULL(z.oact,0) Otros_Actividades, 
                        IFNULL(z.mc,0) Cuestionarios, 
                        IFNULL(z.menc,0) Encuestas, 
                        IFNULL(z.mw,0) Talleres, 
                        IFNULL(z.mt,0) Tareas, 
                        IFNULL(z.mfile,0) Archivos_Recursos, 
                        IFNULL(z.murl,0) "Url", 
                        IFNULL(f.Archivos,0) Archivos,
                        0 video_conferencias,
                        %(desde)s fecha_registro
                    FROM
                        (SELECT 
                            c3.name Facultad, c2.name Escuela, cc.name Programa, c.shortname, c.fullname, c.idnumber, c.visible 
                            ,from_unixtime(c.timecreated) Creacion, from_unixtime(c.startdate) Inicio 
                            ,(SELECT GROUP_CONCAT( CONCAT( u.username, " - ", u.firstname,  " ", u.lastname ) ) 
                            FROM mdl_course             cd
                            JOIN mdl_context            ctx   ON ctx.instanceid = cd.id AND ctx.contextlevel = 50
                            JOIN mdl_role_assignments   ra    ON ctx.id = ra.contextid 
                            JOIN mdl_role               r     ON ra.roleid = r.id
                            JOIN mdl_user               u     ON u.id = ra.userid
                            WHERE (r.id = 3 OR r.id = 4) AND cd.id = c.id
                            GROUP BY c.id
                            ) AS Docentes
                        -- ,COUNT(IF(ra.roleid=5 or ra.roleid=12,ra.userid,NULL))   ne
                        ,COUNT(IF(ra.roleid=3 or ra.roleid=4, ra.userid,NULL))   nd
                        FROM 
                            mdl_course                      c
                        LEFT JOIN mdl_context           ctx   ON ctx.instanceid = c.id AND ctx.contextlevel = 50
                        LEFT JOIN mdl_role_assignments  ra    ON ctx.id = ra.contextid
                        JOIN mdl_course_categories      cc    ON cc.id	= c.category
                        LEFT JOIN (select id, name, idnumber, parent from mdl_course_categories)   c2 ON cc.parent = c2.id
                        LEFT JOIN (select id, name, idnumber, parent from mdl_course_categories)   c3 ON c2.parent = c3.id
                        --     WHERE  1=1
                        GROUP BY c.shortname
                        ) n 
                    LEFT JOIN 
                    (SELECT 
                    c.shortname
                        ,COUNT(IF(m.name IN ("resource", "book", "imscp", "folder", "file", "label", "page", "url"),m.name,NULL))   mrec     --  Recursos
                        ,COUNT(IF(m.name IN ("assign", "assignment", "chat", "choice", "data", "feedback", "forum", 
                                            "glossary", "lesson", "lti", "quiz", "scorm", "survey", "wiki",
                                            "workshop", "attendance", "questionnaire", "scormcloud"),m.name,NULL))       mact   --  Actividades
                        ,COUNT(IF(m.name IN ("resource", "book", "imscp", "folder", "label", "page"),m.name,NULL))        orec   --  Otros Recursos
                        ,COUNT(IF(m.name IN ("assignment", "chat", "data", "feedback", "forum", 
                                            "glossary", "lesson", "lti", "scorm", "wiki",
                                            "attendance", "scormcloud"),m.name,NULL))                                    oact   --  Otros Actividades            ,COUNT(IF(m.name IN ("label"),m.name,NULL))                                                       me     --  Etiquetas
                        ,COUNT(IF(m.name IN ("forum", "chat"),m.name,NULL))                                               mfc    --  Foro y Chat
                        ,COUNT(IF(m.name IN ("attendance"),m.name,NULL))                                                  ma     --  Asistencia
                        ,COUNT(IF(m.name IN ("questionnaire", "quiz", "choice"),m.name,NULL))                             mc     --  Cuestionario
                        ,COUNT(IF(m.name IN ("survey"),m.name,NULL))                                                      menc   --  Encuestas
                        ,COUNT(IF(m.name IN ("workshop"),m.name,NULL))                                                    mw     --  Talleres
                        ,COUNT(IF(m.name IN ("assign"),m.name,NULL))                                                      mt     --  Tareas
                        ,COUNT(IF(m.name IN ("file"),m.name,NULL))                                                        mfile  --  Archivo
                        ,COUNT(IF(m.name IN ("url"),m.name,NULL))                                                         murl   --  URL
                    FROM 
                        mdl_course              c
                        JOIN mdl_course_modules cm  ON  cm.course = c.id 
                        JOIN mdl_modules        m   ON  m.id = cm.module
                                                        and from_unixtime(cm.added) >= %(desde)s			-- Fecha de inicio de aC1o
                                                        and from_unixtime(cm.added) <  %(hasta)s			-- Fecha de tC)rmino periodo
                    GROUP BY c.shortname
                    ) z
                ON n.shortname = z.shortname
                
                LEFT JOIN 
                    (select
                        shortname, /*username, */count(Fuente) Archivos
                    from
                        (select  DISTINCT 
                            c.shortname, /*u.username,*/ 
                            from_unixtime(f.timecreated) Creacion, f.source Fuente
                        from  
                            mdl_files                 f 
                            JOIN mdl_context          ct  ON ct.id = f.contextid
                            JOIN mdl_course_modules   cm  ON cm.id = ct.instanceid 
                            JOIN mdl_course           c   ON c.id  = cm.course 
                            
                            JOIN mdl_user             u   ON u.id = f.userid 
                            JOIN mdl_role_assignments ra  ON ra.userid = u.id 
                            JOIN mdl_role             r   ON r.id = ra.roleid 
                        where 
                                f.component     not in ("user") 
                            and f.source        is not null
                            and ra.roleid       in (3,4,9,10)  -- Profesor principal, secundario, autoridad y editor  
                            and u.username 	not in ("guest","admin","soporte","rarancibia","nsalazarb","17254960")
                            and from_unixtime(f.timecreated) >= %(desde)s			-- Fecha de inicio de aC1o
                            and from_unixtime(f.timecreated) <  %(hasta)s			-- Fecha de tC)rmino de periodo
                            -- and c.shortname = ("11012-1")
                        
                        ) x
                    group by shortname-- , username 
                    ) f 
                ON n.shortname = f.shortname
            where 
                n.visible
            --    and n.shortname in ("62184-1","65064-1")
            --    and z.ma = 0
            order by  n.Facultad, n.Escuela, n.shortname
            """
    
actividades = """
            SELECT 
                    IFNULL(n.idnumber, "") idnumber, 
                    IFNULL(n.Facultad, "") Facultad, 
                    IFNULL(n.Escuela, "") Escuela, 
                    IFNULL(n.Programa, "") Programa,
                    IFNULL(n.fullname, "")  Curso, 
                    IFNULL(n.shortname, "")  seccion_curso,
                    IFNULL(n.Inicio, "") Inicio,
                    IFNULL(n.Docentes, "") Docentes, 
                    IFNULL(n.nd,0) "cantidad_docentes",
                    IFNULL(d.da,0) "Docentes Activos", 
                    IFNULL(d.hdt,0) "Hits Total-cu Docentes", 
                    IFNULL(ROUND((IFNULL(d.hdt,0)/IFNULL(d.da,0.001))/10,0),0) "Ratio_10 Docente", 
                    IFNULL(d.hdp,0) "Hits Periodo-cu Docentes", 
                    n.ne "Estudiantes", 
                    IFNULL(d.ea,0) "Estudiantes Activos", 
                    IFNULL(d.het,0) "Hits Total Estudiantes", 
                    IFNULL(ROUND((IFNULL(d.het,0)/IFNULL(d.ea,0.001))/10,0),0) "Ratio_10 Estudiante" , 
                    IFNULL(d.hep,0) "Hits Periodo Estudiantes", 
                    if ((n.ne>0) AND (ROUND((IFNULL(d.hdt,0)/IFNULL(d.da,0.001))/10,0)>=2 OR ROUND((IFNULL(d.het,0)/IFNULL(d.ea,0.001))/10,0)>=2), "SI", "NO") "Curso Activo",
                    %(registro)s fecha_registro
                from
                    (SELECT 
                        c3.name Facultad, c2.name Escuela, cc.name Programa, c.shortname, c.fullname, c.idnumber, c.visible, from_unixtime(c.startdate) Inicio 
                        ,(SELECT GROUP_CONCAT( CONCAT( u.firstname,  " ", u.lastname ) ) 
                        FROM mdl_course                 cd
                        left JOIN mdl_context           ctx   ON ctx.instanceid = cd.id AND ctx.contextlevel = 50
                        left JOIN mdl_role_assignments  ra    ON ctx.id = ra.contextid
                        left JOIN mdl_role              r     ON ra.roleid = r.id
                        left JOIN mdl_user              u     ON u.id = ra.userid
                        WHERE (r.id=3 OR r.id=4) AND cd.id = c.id
                        GROUP BY c.id
                        ) AS Docentes
                        ,COUNT(IF(ra.roleid=5 or ra.roleid=12,ra.userid,NULL))  ne
                        ,COUNT(IF(ra.roleid=3 or ra.roleid=4,ra.userid,NULL))   nd
                    FROM 
                        mdl_course                      c
                        left JOIN mdl_context           ctx   ON ctx.instanceid = c.id AND ctx.contextlevel = 50
                        left JOIN mdl_role_assignments  ra    ON ctx.id = ra.contextid
                        join mdl_course_categories      cc    ON c.category	= cc.id
                        left JOIN (select id, name, idnumber, parent from mdl_course_categories)   c2 ON cc.parent = c2.id
                        left JOIN (select id, name, idnumber, parent from mdl_course_categories)   c3 ON c2.parent = c3.id
                --     WHERE  1=1
                    group by c.shortname
                    ) n 
                    LEFT JOIN 
                        (SELECT 
                            c.shortname -- ,course.fullname Curso 
                            ,COUNT(distinct IF(ra.roleid=3 or ra.roleid=4, l.userid, NULL))     da    --  "Docentes Activos"
                            ,COUNT(IF((ra.roleid=3 or ra.roleid=4) and 
                                    (l.crud="c" or l.crud="u"), l.userid, NULL))              hdt   --  "Hits Docentes Total"
                            ,COUNT(IF((ra.roleid=3 or ra.roleid=4) and 
                                    (l.crud ="c" or l.crud ="u") and 
                                    (l.timecreated >= UNIX_TIMESTAMP(%(desde)s)) and    
                                    (l.timecreated <  UNIX_TIMESTAMP(%(hasta)s))        
                                    , l.userid, NULL))  hdp                                         --  "Hits Docentes Parcial"
                            ,COUNT(distinct IF(ra.roleid=5, ra.userid, NULL))                   ea    --  "Estudiantes Activos"
                            ,COUNT(IF(ra.roleid=5 or ra.roleid=12, l.userid, NULL))             het   --  "Hits Estudiantes Total"
                            ,COUNT(IF((ra.roleid=5 or ra.roleid=12) and 
                                    (l.timecreated >= UNIX_TIMESTAMP(%(desde)s)) and    
                                    (l.timecreated <  UNIX_TIMESTAMP(%(hasta)s))        
                                    , l.userid, NULL))                                        hep   --  "Hits Estudiantes Parcial"
                        FROM 
                            mdl_course                            c
                            left JOIN mdl_context                 ctx   ON ctx.instanceid = c.id AND ctx.contextlevel = 50
                            left JOIN mdl_role_assignments        ra    ON ctx.id = ra.contextid 
                            left JOIN mdl_logstore_standard_log   l     ON l.courseid = c.id and l.userid = ra.userid 
                        WHERE 
                                l.timecreated >= UNIX_TIMESTAMP(%(desde)s)                -- Fecha Inicio de Año
                            AND l.timecreated <  UNIX_TIMESTAMP(%(hasta)s)                -- Fecha Termino de Periodo
                        GROUP by c.shortname
                        ) d ON n.shortname = d.shortname
                where n.visible 
                order by n.Facultad, n.Escuela, n.shortname
            """