document.addEventListener('DOMContentLoaded', () => {
    const steps = document.querySelectorAll('.step');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const optionCards = document.querySelectorAll('.option-card');
    const documentRequirementsDiv = document.getElementById('documentRequirements');
    const processInfoDiv = document.getElementById('processInfo');
    const showPopupButtons = document.querySelectorAll('.show-popup');
    const closeButtons = document.querySelectorAll('.close-button');

    // Nuevos elementos para el modal de descripción de documentos
    const documentDescriptionModal = document.getElementById('documentDescriptionModal');
    const documentTitle = document.getElementById('documentTitle');
    const documentDescription = document.getElementById('documentDescription');
    const documentImportance = document.getElementById('documentImportance');

    let currentStep = 0;
    let selectedRegularizationType = null; // Para almacenar el tipo de regularización seleccionado

    // Datos de ejemplo para los pasos 2 y 3 (simulando una base de datos o API)
    // Ahora, cada documento tiene un 'name', 'description', y 'importance'
    const data = {
        dfl2: {
            documents: [
                { name: 'Certificado de Dominio Vigente', description: 'Documento emitido por el Conservador de Bienes Raíces que acredita quién es el actual dueño de la propiedad y si tiene hipotecas o prohibiciones.', importance: 'Es el título de propiedad actualizado y fundamental para verificar la titularidad.' },
                { name: 'Certificado de Avalúo Fiscal', description: 'Documento del Servicio de Impuestos Internos (SII) que indica el valor fiscal de la propiedad.', importance: 'Necesario para calcular impuestos y verificar la clasificación de la propiedad según el SII.' },
                { name: 'Copia de planos originales', description: 'Si la propiedad tuvo planos aprobados inicialmente, es crucial tener una copia.', importance: 'Permite comparar la construcción actual con lo que se aprobó originalmente para identificar discrepancias.' },
                { name: 'Permiso de Edificación y Recepción Final', description: 'Si aplica, son los documentos municipales que aprueban la construcción y su finalización.', importance: 'Demuestran que la construcción cumple con las normativas urbanísticas y de edificación.' },
                { name: 'Rol de la Propiedad', description: 'Identificador único de la propiedad asignado por el SII.', importance: 'Es el número clave para todos los trámites relacionados con impuestos y propiedad.' },
                { name: 'Cédula de Identidad del propietario(s)', description: 'Documento de identificación del dueño o dueños de la propiedad.', importance: 'Acredita la identidad del solicitante y su capacidad legal para realizar el trámite.' },
                { name: 'Certificado de No Expropiación', description: 'Emitido por el SERVIU, indica que la propiedad no está afecta a expropiación por utilidad pública.', importance: 'Garantiza que el terreno no será requerido por el Estado para proyectos públicos.' }
            ],
            process: `
                <h3>Proceso de Regularización DFL N°2</h3>
                <ol>
                    <li><strong>Reunir Documentos:</strong> Junta toda la documentación necesaria.</li>
                    <li><strong>Informe Técnico/Planos:</strong> Un arquitecto debe preparar planos y un informe técnico según la normativa DFL N°2.</li>
                    <li><strong>Solicitud Municipal:</strong> Presenta la solicitud y documentos en la Dirección de Obras Municipales (DOM) correspondiente.</li>
                    <li><strong>Revisión DOM:</strong> La DOM revisará los antecedentes. Puede pedir aclaraciones.</li>
                    <li><strong>Permiso de Edificación y Recepción Final (si aplica):</strong> Si la construcción es nueva o sin recepción, se otorgará.</li>
                    <li><strong>Inscripción en CBR:</strong> Con la resolución municipal, inscribe la propiedad en el Conservador de Bienes Raíces (CBR).</li>
                </ol>
            `
        },
        ley18101: {
            documents: [
                { name: 'Certificado de Dominio Vigente', description: 'Documento del CBR que acredita quién es el actual dueño de la propiedad y si tiene hipotecas o prohibiciones.', importance: 'Verifica la titularidad y los gravámenes sobre la propiedad.' },
                { name: 'Certificado de Gravámenes y Prohibiciones', description: 'Documento del CBR que detalla si la propiedad tiene hipotecas, embargos, servidumbres u otras limitaciones.', importance: 'Indispensable para conocer la situación legal de la propiedad y si hay obstáculos para su regularización.' },
                { name: 'Copia de escritura de compraventa (o título anterior)', description: 'Documento legal que demuestra cómo se adquirió la propiedad.', importance: 'Traza la historia de la propiedad y es esencial para el estudio de títulos.' },
                { name: 'Certificado de Avalúo Fiscal Detallado', description: 'Del SII, con el desglose del avalúo del terreno y la construcción.', importance: 'Sirve para determinar el valor tributario y posibles impuestos asociados.' },
                { name: 'Rol de la Propiedad', description: 'Identificador único de la propiedad asignado por el SII.', importance: 'Clave para la identificación tributaria y administrativa de la propiedad.' },
                { name: 'Cédula de Identidad del propietario(s)', description: 'Documento de identificación del dueño o dueños de la propiedad.', importance: 'Acredita la identidad y la capacidad legal del solicitante.' },
                { name: 'Certificado de Deudas de Contribuciones', description: 'Emitido por la Tesorería General de la República, indica si existen deudas por impuestos territoriales (contribuciones).', importance: 'Las deudas de contribuciones pueden impedir la regularización o venta de la propiedad.' },
                { name: 'Planos de la propiedad', description: 'Si existen y están regularizados, ayudan a verificar las dimensiones y distribución.', importance: 'Sirven de base para el saneamiento si la discrepancia es con los planos.' }
            ],
            process: `
                <h3>Proceso de Regularización Ley 18.101</h3>
                <ol>
                    <li><strong>Estudio de Títulos:</strong> Un abogado debe revisar la historia de la propiedad para identificar irregularidades.</li>
                    <li><strong>Reunión de Antecedentes:</strong> Recopilar todos los documentos legales y técnicos.</li>
                    <li><strong>Rectificación o Saneamiento:</strong> Dependiendo del problema, puede requerir juicios de saneamiento, rectificaciones de escrituras, etc.</li>
                    <li><strong>Inscripción en CBR:</strong> Una vez subsanados los problemas, se procede a la inscripción o re-inscripción correcta en el Conservador de Bienes Raíces.</li>
                </ol>
            `
        },
        construccion: {
            documents: [
                { name: 'Certificado de Dominio Vigente', description: 'Del CBR, para confirmar la titularidad del terreno.', importance: 'Asegura que quien solicita la regularización es el dueño legítimo.' },
                { name: 'Certificado de Avalúo Fiscal', description: 'Del SII, para el cálculo de derechos municipales.', importance: 'Necesario para determinar los costos asociados a la regularización.' },
                { name: 'Levantamiento topográfico', description: 'Un mapa detallado del terreno y las construcciones existentes, realizado por un topógrafo.', importance: 'Es la base técnica para la elaboración de nuevos planos y verificar límites y superficies.' },
                { name: 'Planos de arquitectura y cálculo', description: 'Dibujos técnicos y memorias de cálculo de la construcción real, realizados por un arquitecto y/o ingeniero.', importance: 'Demuestran que la construcción cumple con las normativas técnicas y estructurales.' },
                { name: 'Especificaciones técnicas', description: 'Descripción detallada de los materiales y sistemas constructivos utilizados.', importance: 'Complementa los planos y asegura la calidad y cumplimiento de la edificación.' },
                { name: 'Informe de un Profesional Competente', description: 'Declaración jurada de un arquitecto que certifica que la construcción cumple con las normas urbanísticas.', importance: 'Un aval profesional de que la edificación es segura y conforme a la ley.' },
                { name: 'Cédula de Identidad del propietario(s)', description: 'Documento de identificación del dueño o dueños de la propiedad.', importance: 'Acredita la identidad del solicitante y su capacidad legal.' }
            ],
            process: `
                <h3>Proceso de Regularización de Construcción</h3>
                <ol>
                    <li><strong>Levantamiento y Planos:</strong> Contratar a un arquitecto para levantar los planos de lo construido.</li>
                    <li><strong>Informe Técnico:</strong> El arquitecto prepara un informe que indique que la construcción cumple con la normativa.</li>
                    <li><strong>Solicitud de Regularización:</strong> Presentar la solicitud formal en la Dirección de Obras Municipales (DOM).</li>
                    <li><strong>Revisión DOM:</strong> La DOM verifica el cumplimiento de las normativas de urbanismo y construcción.</li>
                    <li><strong>Recepción Municipal:</strong> Una vez aprobada, la DOM emitirá la recepción final.</li>
                    <li><strong>Inscripción en CBR:</strong> Inscribe la recepción final en el Conservador de Bienes Raíces.</li>
                </ol>
            `
        },
        saneamiento: {
            documents: [
                { name: 'Certificado de Dominio Vigente con historia', description: 'Del CBR, mostrando el historial completo de inscripciones de la propiedad.', importance: 'Fundamental para rastrear la cadena de propiedad y cualquier error o vacío.' },
                { name: 'Copia de todas las escrituras y actos relacionados', description: 'Cualquier documento legal que mencione la propiedad, como compraventas, herencias, donaciones, etc.', importance: 'Provee el sustento documental para el análisis legal del problema de título.' },
                { name: 'Certificado de Avalúo Fiscal', description: 'Del SII, para identificar la propiedad.', importance: 'Ayuda a identificar la propiedad de forma tributaria.' },
                { name: 'Certificado de defunción y posesión efectiva', description: 'En casos de propiedades heredadas sin traspasar.', importance: 'Indispensables para acreditar la calidad de heredero y el derecho a la propiedad.' },
                { name: 'Cédula de Identidad del solicitante(s)', description: 'Documento de identificación del dueño o dueños de la propiedad.', importance: 'Acredita la identidad de quien busca sanear el título.' },
                { name: 'Otros documentos que acrediten posesión o derecho', description: 'Recibos de contribuciones, luz, agua, testimonios, etc., que demuestren que se ha ejercido posesión sobre la propiedad.', importance: 'Ayudan a probar la posesión material del inmueble, lo que es clave en muchos juicios de saneamiento.' }
            ],
            process: `
                <h3>Proceso de Saneamiento de Títulos</h3>
                <ol>
                    <li><strong>Estudio Legal:</strong> Un abogado debe realizar un exhaustivo estudio de los títulos para determinar la irregularidad.</li>
                    <li><strong>Identificación del Problema:</strong> Determinar si es un problema de inscripción, herencia, error en escrituras, etc.</li>
                    <li><strong>Vía Legal:</strong> Dependiendo del problema, se puede requerir un juicio de saneamiento (Ley 19.330), rectificaciones de escritura pública, posesiones efectivas, etc.</li>
                    <li><strong>Resolución Judicial/Administrativa:</strong> Obtener la sentencia o resolución que sanee el título.</li>
                    <li><strong>Inscripción Definitiva:</strong> Inscribir la nueva situación de la propiedad en el Conservador de Bienes Raíces.</li>
                </ol>
            `
        }
    };

    // Funciones de navegación de pasos
    function showStep(index) {
        steps.forEach((step, i) => {
            step.classList.toggle('active', i === index);
        });
        currentStep = index;
        updateNavigationButtons();
        updateProgressBar();
    }

    function updateNavigationButtons() {
        prevBtn.disabled = currentStep === 0;
        nextBtn.disabled = currentStep === steps.length - 1;

        if (currentStep === steps.length - 1) {
            nextBtn.textContent = 'Finalizar Guía';
        } else {
            nextBtn.textContent = 'Siguiente';
        }

        // Desactivar el botón Siguiente en el Paso 1 si no hay tipo seleccionado
        if (currentStep === 0 && !selectedRegularizationType) {
            nextBtn.disabled = true;
        }
    }

    function updateProgressBar() {
        const progress = ((currentStep + 1) / steps.length) * 100;
        progressBar.style.width = `${progress}%`;
        progressText.textContent = `Paso ${currentStep + 1} de ${steps.length}: ${steps[currentStep].querySelector('h2').textContent.replace('Paso ' + (currentStep + 1) + ': ', '')}`;
    }

    // Manejo de la selección del tipo de regularización (Paso 1)
    optionCards.forEach(card => {
        card.addEventListener('click', () => {
            optionCards.forEach(c => c.classList.remove('selected')); // Deseleccionar todos
            card.classList.add('selected'); // Seleccionar el clickeado
            selectedRegularizationType = card.dataset.type; // Guardar el tipo
            updateNavigationButtons(); // Habilitar 'Siguiente'

            // Cargar dinámicamente el contenido para los pasos 2 y 3
            if (data[selectedRegularizationType]) {
                // Generar la lista de documentos clickeables para el Paso 2
                let documentsHtml = '<h3>Documentos Requeridos</h3><ul>';
                data[selectedRegularizationType].documents.forEach((doc, index) => {
                    // Usamos data-attributes para almacenar la descripción y la importancia
                    documentsHtml += `<li class="document-item" data-name="${doc.name}" data-description="${doc.description}" data-importance="${doc.importance}">${doc.name}</li>`;
                });
                documentsHtml += '</ul>';
                documentRequirementsDiv.innerHTML = documentsHtml;
                addDocumentClickListener(); // Añadir listener a los nuevos documentos
                
                processInfoDiv.innerHTML = data[selectedRegularizationType].process;
                // addTooltipListeners(); // Re-añadir listeners para tooltips si se generó nuevo contenido aquí
            }
        });
    });

    // Navegación con botones
    nextBtn.addEventListener('click', () => {
        if (currentStep < steps.length - 1) {
            if (currentStep === 0 && !selectedRegularizationType) {
                alert('Por favor, selecciona un tipo de regularización para continuar.');
                return;
            }
            showStep(currentStep + 1);
        } else {
            // Acción al "Finalizar Guía" - podría ser un pop-up de agradecimiento o redirección
            openModal(document.getElementById('contactPopup'));
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    });

    // Función para añadir listeners a los elementos de documento
    function addDocumentClickListener() {
        const documentItems = documentRequirementsDiv.querySelectorAll('.document-item');
        documentItems.forEach(item => {
            item.addEventListener('click', () => {
                // Llenar el modal con la información del documento
                documentTitle.textContent = item.dataset.name;
                documentDescription.textContent = item.dataset.description;
                documentImportance.textContent = item.dataset.importance;
                openModal(documentDescriptionModal); // Abrir el modal
            });
        });
    }

    // Funciones para Modales (Pop-ups)
    function openModal(modalElement) {
        modalElement.classList.add('active');
    }

    function closeModal(modalElement) {
        modalElement.classList.remove('active');
    }

    showPopupButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault(); // Evitar comportamiento predeterminado si es un enlace
            const popupId = button.dataset.popup;
            const modal = document.getElementById(popupId);
            if (modal) {
                openModal(modal);
            }
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal');
            if (modal) {
                closeModal(modal);
            }
        });
    });

    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', (event) => {
        document.querySelectorAll('.modal.active').forEach(modal => {
            if (event.target === modal) {
                closeModal(modal);
            }
        });
    });

    // Tooltips (explicaciones emergentes) - Mejorado para posicionamiento
    function addTooltipListeners() {
        // Remover listeners previos para evitar duplicados si el contenido se recarga
        // (Aunque para el CBR, no se recargará, es buena práctica)
        document.querySelectorAll('.tooltip-trigger').forEach(trigger => {
            trigger.removeEventListener('mouseenter', handleTooltipEnter);
            trigger.removeEventListener('mouseleave', handleTooltipLeave);
        });

        // Añadir listeners para los tooltips
        document.querySelectorAll('.tooltip-trigger').forEach(trigger => {
            trigger.addEventListener('mouseenter', handleTooltipEnter);
            trigger.addEventListener('mouseleave', handleTooltipLeave);
        });
    }

    function handleTooltipEnter(event) {
        const tooltipId = event.target.dataset.tooltipContent;
        const tooltipContentElement = document.querySelector(tooltipId);
        
        if (!tooltipContentElement) return; // Si no encuentra el contenido, salir

        // Crear el elemento tooltip dinámicamente si no existe
        let dynamicTooltip = document.getElementById('dynamic-tooltip');
        if (!dynamicTooltip) {
            dynamicTooltip = document.createElement('div');
            dynamicTooltip.id = 'dynamic-tooltip';
            document.body.appendChild(dynamicTooltip);
        }

        // Aplicar la clase para los estilos base del tooltip
        dynamicTooltip.className = 'tooltip-content'; // Se usa la misma clase CSS

        dynamicTooltip.innerHTML = tooltipContentElement.innerHTML; // Cargar el contenido

        // Posicionar el tooltip
        const triggerRect = event.target.getBoundingClientRect();
        const tooltipWidth = dynamicTooltip.offsetWidth; // Obtener ancho después de cargar contenido
        const tooltipHeight = dynamicTooltip.offsetHeight; // Obtener alto después de cargar contenido

        dynamicTooltip.style.left = `${triggerRect.left + window.scrollX + triggerRect.width / 2}px`;
        dynamicTooltip.style.top = `${triggerRect.top + window.scrollY - tooltipHeight - 10}px`; // 10px encima del trigger
        dynamicTooltip.style.transform = 'translateX(-50%)'; // Centrar horizontalmente

        // Manejo de la posición si el tooltip se sale de la pantalla a la izquierda/derecha
        const bodyRect = document.body.getBoundingClientRect();
        if (triggerRect.left + triggerRect.width / 2 - tooltipWidth / 2 < 0) { // Se sale por la izquierda
            dynamicTooltip.style.left = `${window.scrollX + 10}px`; // Ponerlo a 10px del borde
            dynamicTooltip.style.transform = 'none'; // Desactivar transform para centrar
        } else if (triggerRect.left + triggerRect.width / 2 + tooltipWidth / 2 > bodyRect.width) { // Se sale por la derecha
            dynamicTooltip.style.left = `${window.scrollX + bodyRect.width - tooltipWidth - 10}px`; // Ponerlo a 10px del borde derecho
            dynamicTooltip.style.transform = 'none'; // Desactivar transform para centrar
        }


        dynamicTooltip.style.visibility = 'visible';
        dynamicTooltip.style.opacity = '1';
    }

    function handleTooltipLeave() {
        const dynamicTooltip = document.getElementById('dynamic-tooltip');
        if (dynamicTooltip) {
            dynamicTooltip.style.visibility = 'hidden';
            dynamicTooltip.style.opacity = '0';
        }
    }


    // Inicialización al cargar la página
    showStep(0); // Mostrar el primer paso al inicio
    addTooltipListeners(); // Asegurarse de que los tooltips iniciales funcionen

    // El contenido original del tooltip del CBR se ocultará por CSS con hidden-tooltip-content
});