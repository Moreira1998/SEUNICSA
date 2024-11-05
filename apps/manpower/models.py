from django.db import models

# Modelo Personal
class Personal(models.Model):
    cedula = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    inss = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'

    def __str__(self):
        return self.nombre


# Modelo Cargo
class Cargo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargo'

    def __str__(self):
        return self.nombre


# Modelo Campaña
class Campania(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    fecha = models.DateField()
    vacaciones = models.FloatField()
    aguinaldo = models.FloatField()
    septimo = models.FloatField()
    tonelaje = models.FloatField(null=True, blank=True)
    cambio = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campaña'

    def __str__(self):
        return self.nombre


class Preliminar(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    campania = models.ForeignKey(Campania, on_delete=models.CASCADE)
    total = models.FloatField()

    def calcular_monto(self, porcentaje):
        monto = self.total * porcentaje
        valor = round(monto * self.campania.tonelaje, 3)
        return {'monto': monto, 'valor': valor}

    def indemnizacion(self):
        return self.calcular_monto(self.campania.septimo)

    def aguinaldo(self):
        return self.calcular_monto(self.campania.aguinaldo)

    def vacaciones(self):
        return self.calcular_monto(self.campania.vacaciones)
    
    def salario_base(self):
        indemnizacion = self.indemnizacion()['monto']
        aguinaldo = self.aguinaldo()['monto']
        vacaciones = self.vacaciones()['monto']
        salario = self.total - indemnizacion - aguinaldo - vacaciones
        return round(salario * self.campania.tonelaje, 3)
    
    def sb(self):
        indemnizacion = self.indemnizacion()['monto']
        aguinaldo = self.aguinaldo()['monto']
        vacaciones = self.vacaciones()['monto']
        salario = self.total - indemnizacion - aguinaldo - vacaciones
        return salario
    
    def inss(self):
        return round(self.salario_base() + self.vacaciones()['valor'], 3)

    def total_base(self):
        indemnizacion = self.indemnizacion()['valor']
        aguinaldo = self.aguinaldo()['valor']
        vacaciones = self.vacaciones()['valor']
        salario_base = self.salario_base()
        return round(indemnizacion + aguinaldo + vacaciones + salario_base, 2)

    class Meta:
        verbose_name = 'Preliminar'
        verbose_name_plural = 'Preliminar'

    def __str__(self):
        return f'{self.cargo.nombre} - {self.campania.nombre} - {self.personal}'

    
# Modelo Cargo
class Asistencia(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True)
    campania = models.ForeignKey(Campania, on_delete=models.CASCADE)
    fecha = models.DateField() 

    def __str__(self):
        return f'{self.personal} - {self.fecha}'

# Modelo carga tonelaje 
class Descargue(models.Model):
    campania = models.ForeignKey(Campania, on_delete=models.CASCADE)
    fecha = models.DateField() 
    monto = models.FloatField()

    def carga_restante(self):
        # Obtener el monto total descargado antes de esta fecha (incluyendo esta instancia)
        total_descargado = Descargue.objects.filter(campania=self.campania, fecha__lte=self.fecha).aggregate(total=models.Sum('monto'))['total']
        
        # Si no hay descargas previas, el total descargado es 0
        if total_descargado is None:
            total_descargado = 0
        
        # Restar el monto descargado del tonelaje de la campaña
        return round(self.campania.tonelaje - total_descargado, 2)
    
    class Meta:
        verbose_name = 'Carga tonelaje'
        verbose_name_plural = 'Carga tonelaje'

    def __str__(self):
        return f'{self.campania} - {self.fecha}- {self.monto}'
    
    